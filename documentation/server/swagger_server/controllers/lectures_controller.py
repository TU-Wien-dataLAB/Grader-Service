import connexion
import six

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.lecture import Lecture  # noqa: E501
from swagger_server import util


def lectures_get(semester=None):  # noqa: E501
    """Return all lectures that are available to the user

     # noqa: E501

    :param semester: The semester for which to fetch lectures
    :type semester: str

    :rtype: List[Lecture]
    """
    return 'do some magic!'


def lectures_lect_id_delete(lect_id):  # noqa: E501
    """Delete an existing lecture

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int

    :rtype: Lecture
    """
    return 'do some magic!'


def lectures_lect_id_get(lect_id):  # noqa: E501
    """Return the lecture with specified id

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int

    :rtype: Lecture
    """
    return 'do some magic!'


def lectures_lect_id_put(body, lect_id):  # noqa: E501
    """Update an existing lecture

     # noqa: E501

    :param body: The parameters of the lecture that should be updated.
    :type body: dict | bytes
    :param lect_id: ID of the lecture
    :type lect_id: int

    :rtype: Lecture
    """
    if connexion.request.is_json:
        body = Lecture.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lectures_post(body):  # noqa: E501
    """Create new lecture

     # noqa: E501

    :param body: The parameters of the lecture that is created.
    :type body: dict | bytes

    :rtype: Lecture
    """
    if connexion.request.is_json:
        body = Lecture.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
