import asyncio
import json
from asyncio import Future
from contextlib import contextmanager

from kubernetes.client import V1Pod, CoreV1Api, V1ObjectMeta, V1PodStatus
from traitlets import Callable, Unicode, Integer
from traitlets.config import LoggingConfigurable

from .util import make_pod
from ..local_grader import LocalAutogradeExecutor
from kubernetes import config, client

from ...orm import Lecture, Submission
from ...orm import Assignment

config.load_incluster_config()


class GraderPod(LoggingConfigurable):
    poll_interval = Integer(default_value=1000, allow_none=False,
                            help="Time in ms to wait before status is polled again.").tag(config=True)

    def __init__(self, pod: V1Pod, api: CoreV1Api, **kwargs):
        super().__init__(**kwargs)
        self.pod = pod
        self._client = api
        self.loop = asyncio.get_event_loop()
        self._started_future: Future[bool] = Future(loop=self.loop)
        self._completed_future: Future[bool] = Future(loop=self.loop)
        self._polling_task = self.loop.create_task(self._poll_status())

    @property
    def started(self) -> Future[bool]:
        return self._started_future

    @property
    def completed(self) -> Future[bool]:
        return self._completed_future

    def stop_polling(self) -> None:
        if not self._started_future.done():
            self._started_future.set_result(False)
        if not self._completed_future.done():
            self._completed_future.set_result(False)
        self._polling_task.cancel()

    # https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase
    async def _poll_status(self):
        meta: V1ObjectMeta = self.pod.metadata
        while True:
            status: V1PodStatus = self._client.read_namespaced_pod_status(name=meta.name, namespace=meta.namespace)
            if status.phase == "Running" and not self._started_future.done():
                self._started_future.set_result(True)
            if status.phase == "Succeeded" and not self._started_future.done():
                if not self._started_future.done():
                    self._started_future.set_result(True)
                self._completed_future.set_result(True)
            if status.phase == "Failed":
                self.stop_polling()
            # continue for Unknown and Pending
            await asyncio.sleep(self.poll_interval/1000)


def _get_image_name(lecture: Lecture, assignment: Assignment = None) -> str:
    return f"{lecture.code}_image"


class KubeAutogradeExecutor(LocalAutogradeExecutor):
    image_config_path = Unicode(default_value=None, allow_none=True).tag(config=True)
    default_image_name = Callable(default_value=_get_image_name, allow_none=False).tag(config=True)

    def __init__(self, grader_service_dir: str, submission: Submission, **kwargs):
        super().__init__(grader_service_dir, submission, **kwargs)
        self.assignment = self.submission.assignment
        self.lecture = self.assignment.lecture
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
        pod = make_pod(
            name=self.submission.commit_hash,
            cmd=["/usr/bin/true"],
            image=self.get_image(),
            image_pull_policy=None,
            working_dir="/",
            volumes=None,
            volume_mounts=None,
            labels=None,
            annotations=None,
            tolerations=None,
        )
        self.client.create_namespaced_pod(namespace="default", body=pod)
        return GraderPod(pod, self.client, config=self.config)

    async def _run(self):
        grader_pod = self.start_pod()
        success = await grader_pod.started
        if success:
            self.log.info("Pod has successfully started on the cluster!")
        success = await grader_pod.completed
        if success:
            self.log.info("Pod has successfully completed execution!")
        # TODO: cleanup
