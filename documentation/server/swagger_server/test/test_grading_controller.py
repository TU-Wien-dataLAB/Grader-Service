# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.assignment import Assignment  # noqa: E501
from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.grading_result import GradingResult  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.manual_grading_content import ManualGradingContent  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGradingController(BaseTestCase):
    """GradingController integration test stubs"""

    def test_lectures_lect_id_assignments_a_id_grading_get(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_get

        List student submissions of a lecture
        """
        query_string = [('metadata_only', false),
                        ('latest', false),
                        ('student_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading'.format(lect_id=789, a_id=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_auto_post(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_auto_post

        Request the latest submission to be autograded
        """
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/auto'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_manual_delete(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_manual_delete

        Delete the manual feedback for an assignment
        """
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/manual'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_manual_get(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_manual_get

        Return the manual feedback of a graded assignment
        """
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/manual'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_manual_post(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_manual_post

        Create new manual feedback for an assignment
        """
        body = ManualGradingContent()
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/manual'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_manual_put(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_manual_put

        Update the manual feedback for an assignment
        """
        body = ManualGradingContent()
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/manual'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lectures_lect_id_assignments_a_id_grading_student_id_score_get(self):
        """Test case for lectures_lect_id_assignments_a_id_grading_student_id_score_get

        Return the score of an assignment
        """
        query_string = [('submission_id', 789)]
        response = self.client.open(
            '/v1/lectures/{lect_id}/assignments/{a_id}/grading/{student_id}/score'.format(lect_id=789, a_id=789, student_id='student_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
