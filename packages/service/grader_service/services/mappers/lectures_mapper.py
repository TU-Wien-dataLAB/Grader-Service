from grader_service.api.models import LectureListItemDto
from grader_service.orm import Lecture


def to_lecture_list_item_dto(lecture: Lecture, assignment_count, student_count):
    return LectureListItemDto(
        lecture.id, lecture.name, lecture.code, lecture.state, assignment_count, student_count
    )
