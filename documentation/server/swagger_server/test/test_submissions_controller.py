# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.feedback import Feedback  # noqa: E501
from swagger_server.models.submission import Submission  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSubmissionsController(BaseTestCase):
    """SubmissionsController integration test stubs"""

    def test_lectures_lect_id_assignments_a_id_feedback_get(self):
        """Test case for lectures_lect_id_assignments_a_id_feedback_get

        Return the feedback of an assignment
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/feedback'.format(lect_id=789, a_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_submissions_get(self):
        """Test case for lectures_lect_id_assignments_a_id_submissions_get

        Return the submissions of an assignment
        """
        query_string = [('latest', false)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/submissions'.format(lect_id=789, a_id=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_submissions_post(self):
        """Test case for lectures_lect_id_assignments_a_id_submissions_post

        Request assignment to be submitted
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/submissions'.format(lect_id=789, a_id=789),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
