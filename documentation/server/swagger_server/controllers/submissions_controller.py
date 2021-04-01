import connexion
import six

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.feedback import Feedback  # noqa: E501
from swagger_server.models.submission import Submission  # noqa: E501
from swagger_server import util


def lectures_lect_id_assignments_a_id_feedback_get(lect_id, a_id):  # noqa: E501
    """Return the feedback of an assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int

    :rtype: List[Feedback]
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_submissions_get(lect_id, a_id, latest=None):  # noqa: E501
    """Return the submissions of an assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param latest: Only return the latest submission
    :type latest: bool

    :rtype: Submission
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_submissions_post(lect_id, a_id):  # noqa: E501
    """Request assignment to be submitted

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int

    :rtype: None
    """
    return 'do some magic!'
