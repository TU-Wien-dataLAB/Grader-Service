import json
import shutil
from grader_labextension.registry import register_handler
from grader_labextension.handlers.base_handler import ExtensionBaseHandler
from grader_labextension.services.request import RequestService
import tornado
import os

from tornado.httpclient import HTTPError


@register_handler(path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/?")
class AssignmentBaseHandler(ExtensionBaseHandler):
    async def get(self, lecture_id: int):
        """Sends a get request to the grader service and returns assignments of the lecture

        :param lecture_id: id of the lecture
        :type lecture_id: int
        """
        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments",
                header=self.grader_authentication_header,
            )

            lecture = await self.request_service.request(
                "GET",
                f"{self.service_base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return

        # Create directories for every assignment
        try:
            dirs = set(filter(lambda e: e[0] != ".", os.listdir(os.path.expanduser(f'{self.root_dir}/{lecture["code"]}'))))
            for assignment in response:
                if assignment["id"] not in dirs:
                    self.log.info(f'Creating directory {self.root_dir}/{lecture["code"]}/{assignment["id"]}')
                    os.makedirs(
                        os.path.expanduser(f'{self.root_dir}/{lecture["code"]}/{assignment["id"]}'), exist_ok=True
                    )
                try:
                    dirs.remove(assignment["id"])
                except KeyError:
                    pass
        except FileNotFoundError:
            pass
            
        self.write(json.dumps(response))

    async def post(self, lecture_id: int):
        """Sends post-request to the grader service to create an assignment

        :param lecture_id: id of the lecture in which the new assignment is
        :type lecture_id: int
        """        

        data = tornado.escape.json_decode(self.request.body)
        try:
            response = await self.request_service.request(
                method="POST",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments",
                body=data,
                header=self.grader_authentication_header,
            )

            lecture = await self.request_service.request(
                "GET",
                f"{self.service_base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        # if we did not get an error when creating the assignment (i.e. the user is authorized etc.) then we can create the directory structure if it does not exist yet
        os.makedirs(
            os.path.expanduser(f'{self.root_dir}/{lecture["code"]}/{response["id"]}'),
            exist_ok=True
        )
        os.makedirs(
            os.path.expanduser(f"{self.root_dir}/source/{lecture['code']}/{response['id']}"),
            exist_ok=True,
        )
        os.makedirs(
            os.path.expanduser(f"{self.root_dir}/release/{lecture['code']}/{response['id']}"),
            exist_ok=True,
        )
        self.write(json.dumps(response))


@register_handler(
    path=r"\/lectures\/(?P<lecture_id>\d*)\/assignments\/(?P<assignment_id>\d*)\/?"
)
class AssignmentObjectHandler(ExtensionBaseHandler):
    async def put(self, lecture_id: int, assignment_id: int):
        """Sends a PUT-request to the grader service to update a assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        """        

        data = tornado.escape.json_decode(self.request.body)
        try:
            response = await self.request_service.request(
                method="PUT",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                body=data,
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.write(json.dumps(response))

    async def get(self, lecture_id: int, assignment_id: int):
        """Sends a GET-request to the grader service to get a specific assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the specific assignment
        :type assignment_id: int
        """        

        query_params = RequestService.get_query_string(
            {
                "instructor-version": self.get_argument("instructor-version", None),
                "metadata-only": self.get_argument("metadata-only", None),
            }
        )

        try:
            response = await self.request_service.request(
                method="GET",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments/{assignment_id}{query_params}",
                header=self.grader_authentication_header,
            )
            lecture = await self.request_service.request(
                "GET",
                f"{self.service_base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        
        os.makedirs(
            os.path.expanduser(f'{self.root_dir}/{lecture["code"]}/{response["id"]}'),
            exist_ok=True
        )
        self.write(json.dumps(response))

    async def delete(self, lecture_id: int, assignment_id: int):
        """Sends a DELETE-request to the grader service to "soft"-delete a assignment

        :param lecture_id: id of the lecture
        :type lecture_id: int
        :param assignment_id: id of the assignment
        :type assignment_id: int
        """        

        try:
            assignment = await self.request_service.request(
                method="GET",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
            )
            lecture = await self.request_service.request(
                "GET",
                f"{self.service_base_url}/lectures/{lecture_id}",
                header=self.grader_authentication_header,
            )
            response = await self.request_service.request(
                method="DELETE",
                endpoint=f"{self.service_base_url}/lectures/{lecture_id}/assignments/{assignment_id}",
                header=self.grader_authentication_header,
                decode_response=False
            )
        except HTTPError as e:
            self.set_status(e.code)
            self.write_error(e.code)
            return
        self.log.warn(f'Deleting directory {self.root_dir}/{lecture["code"]}/{assignment["id"]}')
        shutil.rmtree(os.path.expanduser(f'{self.root_dir}/{lecture["code"]}/{assignment["id"]}'), ignore_errors=True)
        self.write("OK")


