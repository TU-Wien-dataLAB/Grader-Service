import os

from grader_service.autograding.kube.kube_grader import KubeAutogradeExecutor
from grader_service.autograding.local_grader import LocalAutogradeExecutor, LocalProcessAutogradeExecutor

c.GraderService.service_host = "127.0.0.1"
# existing directory to use as the base directory for the grader service
config_dir = os.path.dirname(__file__)
service_dir = os.path.join(config_dir, "service_dir")
c.GraderService.grader_service_dir = service_dir

c.GraderServer.hub_service_name = "grader"
c.GraderServer.hub_api_token = "7572f93a2e7640999427d9289c8318c0"
c.GraderServer.hub_api_url = "http://127.0.0.1:8081/hub/api"
c.GraderServer.hub_base_url = "/"

c.LocalAutogradeExecutor.base_input_path = os.path.expanduser(os.path.join(service_dir, "convert_in"))
c.LocalAutogradeExecutor.base_output_path = os.path.expanduser(os.path.join(service_dir, "convert_out"))

assert issubclass(KubeAutogradeExecutor, LocalAutogradeExecutor)
c.RequestHandlerConfig.autograde_executor_class = LocalProcessAutogradeExecutor
c.KubeAutogradeExecutor.kube_context = "minikube"
c.KubeAutogradeExecutor.default_image_name = lambda l, a: "s210.dl.hpc.tuwien.ac.at/grader/grader-notebook-minimal:arm"
