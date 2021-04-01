import connexion
import six

from swagger_server.models.assignment import Assignment  # noqa: E501
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.grading_result import GradingResult  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.manual_grading_content import ManualGradingContent  # noqa: E501
from swagger_server import util


def lectures_lect_id_assignments_a_id_grading_get(lect_id, a_id, metadata_only=None, latest=None, student_id=None):  # noqa: E501
    """List student submissions of a lecture

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param metadata_only: Only return the metadata information of the submissions
    :type metadata_only: bool
    :param latest: Only return the latest submission of each student
    :type latest: bool
    :param student_id: Specify the student id
    :type student_id: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_auto_post(lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Request the latest submission to be autograded

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the submission that should be autograded instead of latest
    :type submission_id: int

    :rtype: List[Assignment]
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_manual_delete(lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Delete the manual feedback for an assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the the submission that should be manually graded instead of latest
    :type submission_id: int

    :rtype: None
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_manual_get(lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Return the manual feedback of a graded assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the the submission that should be manually graded instead of latest
    :type submission_id: int

    :rtype: ManualGradingContent
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_manual_post(body, lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Create new manual feedback for an assignment

     # noqa: E501

    :param body: The content of the manual grading.
    :type body: dict | bytes
    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the the submission that should be manually graded instead of latest
    :type submission_id: int

    :rtype: ManualGradingContent
    """
    if connexion.request.is_json:
        body = ManualGradingContent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_manual_put(body, lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Update the manual feedback for an assignment

     # noqa: E501

    :param body: The content of the manual grading to be updated.
    :type body: dict | bytes
    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the the submission that should be manually graded instead of latest
    :type submission_id: int

    :rtype: ManualGradingContent
    """
    if connexion.request.is_json:
        body = ManualGradingContent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_grading_student_id_score_get(lect_id, a_id, student_id, submission_id=None):  # noqa: E501
    """Return the score of an assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param student_id: ID of the student that is enroled in the lecture
    :type student_id: str
    :param submission_id: Specify the the submission that should be returned instead of latest
    :type submission_id: int

    :rtype: GradingResult
    """
    return 'do some magic!'
