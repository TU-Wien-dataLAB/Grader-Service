# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import asyncio
import json
import os
import shutil
import inspect
import warnings
from asyncio import Task, run

from kubernetes.client import (V1Pod, CoreV1Api, V1ObjectMeta,
                               V1PodStatus, ApiException)
from traitlets import Callable, Unicode, Integer, List, Dict
from traitlets.config import LoggingConfigurable
from urllib3.exceptions import MaxRetryError

from grader_service.autograding.docker_grader import DockerImageExecutor
from grader_service.autograding.kube.util import (make_pod,
                                                  get_current_namespace)
from grader_service.autograding.local_grader import (LocalAutogradeExecutor,
                                                     rm_error)
from kubernetes import config

from grader_service.orm import Lecture, Submission
from grader_service.orm import Assignment


class GraderPod(LoggingConfigurable):
    """
    Wrapper for a kubernetes pod that supports polling of the pod's status.
    """
    poll_interval = Integer(default_value=1000,
                            allow_none=False,
                            help="Time in ms to wait before "
                                 "status is polled again.").tag(config=True)

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
            status: V1PodStatus = \
                self._client.read_namespaced_pod_status(
                    name=meta.name,
                    namespace=meta.namespace).status

            if status.phase == "Succeeded" or status.phase == "Failed":
                return status.phase
            # continue for Running, Unknown and Pending
            await asyncio.sleep(self.poll_interval / 1000)


class KubeAutogradeExecutor(DockerImageExecutor):
    """
    Runs an autograde job in a kubernetes cluster as a pod.
    The cluster has to have a shared persistent
    volume claim that is mounted in the input
    and output directories so that both the service and
    the executor pods have access to the files.
    The service account of the grader service has to have
    permission to get, update, create and delete pods, pod status and pod logs.
    """
    kube_context = Unicode(default_value=None, allow_none=True,
                           help="Kubernetes context to load config from. "
                                "If the context is None (default), "
                                "the incluster config "
                                "will be used.").tag(config=True)

    resolve_node_selector = Callable(default_value=lambda _: None, allow_none=False,
                                     help="""Function that takes a lecture as input and outputs a node selector for 
                                     this lecture. The returned value has to be a dict[str, str] or None and is directly 
                                     passed to the Kubernetes API.""").tag(config=True)

    volume = Dict(default_value={},
                  allow_none=False).tag(config=True)

    extra_volumes = List(default_value=[],
                         allow_none=False).tag(config=True)

    extra_volume_mounts = List(default_value=[],
                               allow_none=False).tag(config=True)

    convert_executable = Unicode("grader-convert",
                                 allow_none=False).tag(config=True)

    namespace = Unicode(default_value=None, allow_none=True,
                        help="Namespace to deploy grader pods into. "
                             "If changed, correct roles to Serviceaccount "
                             "need to be applied.").tag(config=True)
    uid = Integer(default_value=1000, allow_none=False,
                  help="The User ID for the grader container").tag(config=True)

    def __init__(self, grader_service_dir: str,
                 submission: Submission, **kwargs):
        super().__init__(grader_service_dir, submission, **kwargs)
        warnings.warn(
            "KubeAutogradeExecutor has been deprecated in favor of DockerAutogradeExecutor in conjunction with "
            "Celery workers!", DeprecationWarning
        )

        if self.kube_context is None:
            self.log.info(f"Loading in-cluster config for kube executor "
                          f"of submission {self.submission.id}")
            config.load_incluster_config()
        else:
            self.log.info(
                f"Loading cluster config '{self.kube_context}' "
                f"for kube executor of submission {self.submission.id}")
            config.load_kube_config(context=self.kube_context)
        self.client = CoreV1Api()

        if self.namespace is None:
            self.log.info(f"Setting Namespace "
                          f"for submission {self.submission.id}")
            self.namespace = get_current_namespace()

    def start_pod(self) -> GraderPod:
        """
        Starts a pod in the default namespace
        with the commit hash as the name of the pod.
        The image is determined by the get_image method.
        :return:
        """
        # The output path will not exist in the pod
        command = [self.convert_executable, "autograde", "-i",
                   self.input_path, "-o", self.output_path,
                   "-p", "*.ipynb",
                   f"--copy_files={self.assignment.allow_files}",
                   "--log-level=INFO",
                   f"--ExecutePreprocessor.timeout={self.timeout_func(self.assignment.lecture)}"]

        # command = "sleep 10000"

        volumes = [self.volume] + self.extra_volumes

        volume_mounts = [{"name": "data", "mountPath": self.input_path,
                          "subPath": self.relative_input_path +
                                     "/submission_" + str(self.submission.id)},
                         {"name": "data", "mountPath": self.output_path,
                          "subPath": self.relative_output_path +
                                     "/submission_" + str(self.submission.id)}]
        volume_mounts = volume_mounts + self.extra_volume_mounts

        pod = make_pod(
            name=self.submission.commit_hash,
            cmd=command,
            image=self.get_image(),
            image_pull_policy=None,
            working_dir="/",
            volumes=volumes,
            volume_mounts=volume_mounts,
            labels=None,
            annotations=None,
            node_selector=self.resolve_node_selector(self.lecture),
            tolerations=None,
            run_as_user=self.uid,
        )

        self.log.info(f"Starting pod {pod.metadata.name}"
                      f" with command: {command}")
        pod = self.client.create_namespaced_pod(namespace=self.namespace,
                                                body=pod)
        return GraderPod(pod, self.client, config=self.config)

    async def _run(self):
        """
        Runs the autograding process in a kubernetes pod
        which has to have access to the files in the
        input and output directory through a persistent volume claim.
        :return: Coroutine
        """
        if os.path.exists(self.output_path):
            shutil.rmtree(self.output_path, onerror=rm_error)

        os.makedirs(self.output_path, exist_ok=True)

        self._write_gradebook(self._put_grades_in_assignment_properties())

        grader_pod = None
        try:
            grader_pod = self.start_pod()
            self.log.info(f"Started pod {grader_pod.name} in namespace "
                          f"{grader_pod.namespace}")
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
            if error_message["reason"] != "AlreadyExists" \
                    and grader_pod is not None:
                try:
                    namespace = grader_pod.namespace
                    self.client.delete_namespaced_pod(name=grader_pod.name,
                                                      namespace=namespace)
                except ApiException:
                    pass
            self.log.error(f'{error_message["reason"]}: '
                           f'{error_message["message"]}')
            raise RuntimeError("Pod has failed execution!")
        except MaxRetryError:
            self.log.error("Kubernetes client could not connect to cluster! "
                           "Is it running and specified correctly?")
            raise RuntimeError("Pod has failed execution!")

    def _delete_pod(self, pod: GraderPod):
        """
        Deletes the pod from the cluster after successful or failed execution.
        :param pod: The pod to delete.
        :return: None
        """
        self.log.info(
            f"Deleting pod '{pod.name}' in namespace '{pod.namespace}' "
            f"after execution status {pod.polling.result()}")
        self.client.delete_namespaced_pod(name=pod.name,
                                          namespace=pod.namespace)

    def _get_pod_logs(self, pod: GraderPod) -> str:
        """
        Returns the logs of the pod that were output during execution.
        :param pod: The pod to retrieve the logs from.
        :return: The logs as a string.
        """
        api_response: str = \
            self.client.read_namespaced_pod_log(name=pod.name,
                                                namespace=pod.namespace)
        return api_response.strip()
