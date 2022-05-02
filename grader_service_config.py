import os

from grader_service.autograding.local_grader import LocalAutogradeExecutor

c.GraderService.service_host = "grader_service"
# existing directory to use as the base directory for the grader service
service_dir = os.path.expanduser("/var/lib/grader-service")
c.GraderService.grader_service_dir = service_dir

c.GraderServer.hub_service_name = "grader"
c.GraderServer.hub_api_token = "7e272a9df62444de9d2d111b5ff6e70f"
c.GraderServer.hub_api_url = "http://jupyterlab:8000/hub/api"
c.GraderServer.hub_base_url = "http://jupyterlab:8000"

c.LocalAutogradeExecutor.base_input_path = os.path.expanduser(os.path.join(service_dir, "convert_in"))
c.LocalAutogradeExecutor.base_output_path = os.path.expanduser(os.path.join(service_dir, "convert_out"))
c.RequestHandlerConfig.autograde_executor_class = LocalAutogradeExecutor
