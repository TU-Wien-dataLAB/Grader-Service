import connexion
import six

from swagger_server.models.assignment import Assignment  # noqa: E501
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def lectures_lect_id_assignments_a_id_delete(lect_id, a_id):  # noqa: E501
    """Delete an existing assignment

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int

    :rtype: None
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_get(lect_id, a_id, instuctor_version=None, metadata_only=None, include_submissions=None):  # noqa: E501
    """Request the assignment to be fetched

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int
    :param instuctor_version: Fetch the instructor version of the assignment
    :type instuctor_version: bool
    :param metadata_only: Only return the assignment information and don&#x27;t fetch it
    :type metadata_only: bool
    :param include_submissions: Include past submissions of the assignment
    :type include_submissions: bool

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def lectures_lect_id_assignments_a_id_put(body, lect_id, a_id):  # noqa: E501
    """Update an existing assignment (also handles release)

     # noqa: E501

    :param body: The parameters of the assignment that should be updated.
    :type body: dict | bytes
    :param lect_id: ID of the lecture
    :type lect_id: int
    :param a_id: ID of the assignment in the lecture
    :type a_id: int

    :rtype: Assignment
    """
    if connexion.request.is_json:
        body = Assignment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def lectures_lect_id_assignments_get(lect_id):  # noqa: E501
    """Return the assignments of a specific lecture

     # noqa: E501

    :param lect_id: ID of the lecture
    :type lect_id: int

    :rtype: List[Assignment]
    """
    return 'do some magic!'


def lectures_lect_id_assignments_post(body, lect_id):  # noqa: E501
    """Request creation of an assignment

     # noqa: E501

    :param body: The initial state of an assignment. Every field will be empty except &#x60;due_date&#x60; and &#x60;name&#x60;.
    :type body: dict | bytes
    :param lect_id: ID of the lecture
    :type lect_id: int

    :rtype: Assignment
    """
    if connexion.request.is_json:
        body = Assignment.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
