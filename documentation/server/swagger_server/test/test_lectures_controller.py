# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.lecture import Lecture  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLecturesController(BaseTestCase):
    """LecturesController integration test stubs"""

    def test_lectures_get(self):
        """Test case for lectures_get

        Return all lectures that are available to the user
        """
        query_string = [('semester', 'semester_example')]
        response = self.client.open(
            '/v1/lectures',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_delete(self):
        """Test case for lectures_lect_id_delete

        Delete an existing lecture
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}'.format(lect_id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_get(self):
        """Test case for lectures_lect_id_get

        Return the lecture with specified id
        """
        response = self.client.open(
            '/v1/lectures/{lect_id}'.format(lect_id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_put(self):
        """Test case for lectures_lect_id_put

        Update an existing lecture
        """
        body = Lecture()
        response = self.client.open(
            '/v1/lectures/{lect_id}'.format(lect_id=789),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_post(self):
        """Test case for lectures_post

        Create new lecture
        """
        body = Lecture()
        response = self.client.open(
            '/v1/lectures',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
