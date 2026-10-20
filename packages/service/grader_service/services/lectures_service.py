from grader_service.services.file_services.base_file_service import FileService


class LecturesService:
    def __init__(self, session_maker, file_service: FileService):
        self.session_maker = session_maker
        self.file_service = file_service

    def get_all_lectures(self):
        pass
