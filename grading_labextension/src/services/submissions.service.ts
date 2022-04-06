import { Assignment } from '../model/assignment';
import { Lecture } from '../model/lecture';
import { Submission } from '../model/submission';
import { request, HTTPMethod } from './request.service';

export function submitAssignment(lecture: Lecture, assignment: Assignment) {
  return request<void>(
    HTTPMethod.PUT,
    `/lectures/${lecture.id}/assignments/${assignment.id}/push/assignment`
  );
}

export async function pullFeedback(
  lecture: Lecture,
  assignment: Assignment,
  submission: Submission
) {
  return request<void>(
    HTTPMethod.GET,
    `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${submission.id}/pull/feedback`
  );
}

export function getSubmissions(
  lecture: Lecture,
  assignment: Assignment,
  latest = false
): Promise<Submission[]> {
  let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;
  if (latest) {
    const searchParams = new URLSearchParams({
      latest: String(latest)
    });
    url += '?' + searchParams;
  }
  return request<any>(HTTPMethod.GET, url);
}

export function getAllSubmissions(
  lecture: Lecture,
  assignment: Assignment,
  latest = false,
  instructor = true
): Promise<Submission[]> {
  let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;

  if (latest || instructor) {
    const searchParams = new URLSearchParams({
      'instructor-version': String(instructor),
      latest: String(latest)
    });
    url += '?' + searchParams;
  }
  return request<Submission[]>(HTTPMethod.GET, url);
}

export function getFeedback(
  lecture: Lecture,
  assignment: Assignment,
  latest = false,
  instructor = false
): Promise<any> {
  let url = `/lectures/${lecture.id}/assignments/${assignment.id}/feedback`;
  if (latest || instructor) {
    const searchParams = new URLSearchParams({
      'instructor-version': String(instructor),
      latest: String(latest)
    });
    url += '?' + searchParams;
  }
  return request<any>(HTTPMethod.GET, url);
}

export function getProperties(
  lectureId: number,
  assignmentId: number,
  submissionId: number
): Promise<object> {
  const url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}/properties`;
  return request<object>(HTTPMethod.GET, url);
}

export function updateProperties(
  lectureId: number,
  assignmentId: number,
  submissionId: number,
  properties: object
): Promise<Submission> {
  const url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}/properties`;
  return request<Submission>(HTTPMethod.PUT, url, properties);
}

export function getSubmission(
  lectureId: number,
  assignmentId: number,
  submissionId: number
): Promise<Submission> {
  const url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}`;
  return request<object>(HTTPMethod.GET, url);
}

export function updateSubmission(
  lectureId: number,
  assignmentId: number,
  submissionId: number,
  sub: Submission
): Promise<Submission> {
  const url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}`;
  return request<Submission>(HTTPMethod.PUT, url, sub);
}