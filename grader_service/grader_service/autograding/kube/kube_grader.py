import asyncio
import json
import os
import shlex
import shutil
from asyncio import Future, Task
from contextlib import contextmanager
from pathlib import Path

from kubernetes.client import V1Pod, CoreV1Api, V1ObjectMeta, V1PodStatus, ApiException
from traitlets import Callable, Unicode, Integer, Dict, List
from traitlets.config import LoggingConfigurable
from urllib3.exceptions import MaxRetryError

from grader_service.autograding.kube.util import make_pod
from grader_service.autograding.local_grader import LocalAutogradeExecutor, rm_error
from kubernetes import config, client

from grader_service.orm import Lecture, Submission
from grader_service.orm import Assignment


class GraderPod(LoggingConfigurable):
    poll_interval = Integer(default_value=1000, allow_none=False,
                            help="Time in ms to wait before status is polled again.").tag(config=True)

    def __init__(self, pod: V1Pod, api: CoreV1Api, **kwargs):
        super().__init__(**kwargs)
        self.pod = pod
        self._client = api
        self.loop = asyncio.get_event_loop()
        self._polling_task = self.loop.create_task(self._poll_status())

    def stop_polling(self) -> None:
        self._polling_task.cancel()

    @property
    def polling(self) -> Task:
        return self._polling_task

    @property
    def name(self) -> str:
        return self.pod.metadata.name

    @property
    def namespace(self) -> str:
        return self.pod.metadata.namespace

    # https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase
    async def _poll_status(self) -> str:
        meta: V1ObjectMeta = self.pod.metadata
        while True:
            status: V1PodStatus = self._client.read_namespaced_pod_status(name=meta.name,
                                                                          namespace=meta.namespace).status
            if status.phase == "Succeeded" or status.phase == "Failed":
                return status.phase
            # continue for Running, Unknown and Pending
            await asyncio.sleep(self.poll_interval / 1000)


def _get_image_name(lecture: Lecture, assignment: Assignment = None) -> str:
    return f"{lecture.code}_image"


class KubeAutogradeExecutor(LocalAutogradeExecutor):
    image_config_path = Unicode(default_value=None, allow_none=True).tag(config=True)
    default_image_name = Callable(default_value=_get_image_name, allow_none=False).tag(config=True)
    kube_context = Unicode(default_value=None, allow_none=True,
                           help="Kubernetes context to load config from. " +
                                "If the context is None (default), the incluster config will be used.").tag(config=True)
    volumes = List(default_value=[], allow_none=False).tag(config=True)
    volume_mounts = List(default_value=[], allow_none=False).tag(config=True)

    def __init__(self, grader_service_dir: str, submission: Submission, **kwargs):
        super().__init__(grader_service_dir, submission, **kwargs)
        self.assignment = self.submission.assignment
        self.lecture = self.assignment.lecture

        if self.kube_context is None:
            self.log.info(f"Loading in-cluster config for kube executor of submission {self.submission.id}")
            config.load_incluster_config()
        else:
            self.log.info(
                f"Loading cluster config '{self.kube_context}' for kube executor of submission {self.submission.id}")
            config.load_kube_config(context=self.kube_context)
        self.client = CoreV1Api()

    def get_image(self) -> str:
        cfg = {}
        if self.image_config_path is not None:
            with open(self.image_config_path, "r") as f:
                cfg = json.load(f)
        try:
            lecture_cfg = cfg[self.lecture.code]
            if isinstance(lecture_cfg, str):
                return lecture_cfg
            else:
                return lecture_cfg[self.assignment.name]
        except KeyError:
            return self.default_image_name(self.lecture, self.assignment)

    def start_pod(self) -> GraderPod:
        # The output path will not exist in the pod
        command = f'{self.convert_executable} autograde ' \
                  f'-i "{self.input_path}" ' \
                  f'-o "{self.output_path}" ' \
                  f'-p "*.ipynb" --log-level=INFO'
        # command = "sleep 10000"
        pod = make_pod(
            name=self.submission.commit_hash,
            cmd=shlex.split(command),
            image=self.get_image(),
            image_pull_policy=None,
            working_dir="/",
            volumes=self.volumes,
            volume_mounts=self.volume_mounts,
            labels=None,
            annotations=None,
            tolerations=None,
        )
        self.log.info(f"Starting pod {pod.metadata.name} with command: {command}")
        pod = self.client.create_namespaced_pod(namespace="default", body=pod)
        return GraderPod(pod, self.client, config=self.config)

    async def _run(self):
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path, onerror=rm_error)

        os.mkdir(self.output_path)
        self._write_gradebook()

        grader_pod = None
        try:
            grader_pod = self.start_pod()
            self.log.info(f"Started pod {grader_pod.name} in namespace {grader_pod.namespace}")
            status = await grader_pod.polling
            self.grading_logs = self._get_pod_logs(grader_pod)
            self.log.info("Pod logs:\n" + self.grading_logs)
            if status == "Succeeded":
                self.log.info("Pod has successfully completed execution!")
            else:
                self.log.info("Pod has failed execution:")
                self._delete_pod(grader_pod)
                raise RuntimeError("Pod has failed execution!")
            # cleanup
            self._delete_pod(grader_pod)
        except ApiException as e:
            error_message = json.loads(e.body)
            if error_message["reason"] != "AlreadyExists" and grader_pod is not None:
                try:
                    self.client.delete_namespaced_pod(name=grader_pod.name, namespace=grader_pod.namespace)
                except ApiException:
                    pass
            self.log.error(f'{error_message["reason"]}: {error_message["message"]}')
            raise RuntimeError("Pod has failed execution!")
        except MaxRetryError:
            self.log.error("Kubernetes client could not connect to cluster! Is it running and specified correctly?")
            raise RuntimeError("Pod has failed execution!")

    def _delete_pod(self, pod: GraderPod):
        self.log.info(
            f"Deleting pod '{pod.name}' in namespace '{pod.namespace}' after execution status {pod.polling.result()}")
        self.client.delete_namespaced_pod(name=pod.name, namespace=pod.namespace)

    def _get_pod_logs(self, pod: GraderPod) -> str:
        api_response: str = self.client.read_namespaced_pod_log(name=pod.name, namespace=pod.namespace)
        return api_response.strip()
