# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.assignment import Assignment  # noqa: E501
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAssignmentsController(BaseTestCase):
    """AssignmentsController integration test stubs"""

    def test_lectures_lect_id_assignments_a_id_delete(self):
        """Test case for lectures_lect_id_assignments_a_id_delete

        Delete an existing assignment
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}'.format(lect_id=789, a_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_get(self):
        """Test case for lectures_lect_id_assignments_a_id_get

        Request the assignment to be fetched
        """
        query_string = [('instuctor_version', false),
                        ('metadata_only', false),
                        ('include_submissions', false)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}'.format(lect_id=789, a_id=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_put(self):
        """Test case for lectures_lect_id_assignments_a_id_put

        Update an existing assignment (also handles release)
        """
        body = Assignment()
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}'.format(lect_id=789, a_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_get(self):
        """Test case for lectures_lect_id_assignments_get

        Return the assignments of a specific lecture
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments'.format(lect_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_post(self):
        """Test case for lectures_lect_id_assignments_post

        Request creation of an assignment
        """
        body = Assignment()
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments'.format(lect_id=789),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
