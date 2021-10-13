import { Observable } from "rxjs";
import { map } from "rxjs/operators";
import { Assignment } from "../model/assignment";
import { Feedback } from "../model/feedback";
import { Lecture } from "../model/lecture";
import { Submission } from "../model/submission";
import { User } from "../model/user";
import { request, HTTPMethod } from "./request.service";


  export function submitAssignment(lecture: Lecture, assignment : Assignment) {
    return request<void>(HTTPMethod.PUT, `/lectures/${lecture.id}/assignments/${assignment.id}/push/assignment`)
  }

  export async function fetchFeedback(lecture: Lecture, assignment: Assignment, submission: Submission) {
    return request<void>(HTTPMethod.GET,`/lectures/${lecture.id}/assignments/${assignment.id}/grading/${submission.id}/feedback`)
  }

  export function getSubmissions(lecture: Lecture, assignment : Assignment, latest: boolean = false): Observable<{user: User, submissions: Submission[]}> {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;
    if (latest) {
      let searchParams = new URLSearchParams({
        "latest": String(latest)
      })
      url += '?' + searchParams;
    }
    return request<{user: User, submissions: Submission[]}[]>(HTTPMethod.GET, url).pipe(map(array => array[0]))
  }

  export function getAllSubmissions(lecture: Lecture, assignment : Assignment, latest: boolean = false, instructor: boolean = true): Observable<{user: User, submissions: Submission[]}[]> {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;

    if (latest || instructor) {
      let searchParams = new URLSearchParams({
        "instructor-version": String(instructor),
        "latest": String(latest)
      })
      url += '?' + searchParams;
    }
    return request<{user: User, submissions: Submission[]}[]>(HTTPMethod.GET, url)

  }

  export function getFeedback(lecture: Lecture, assignment : Assignment, latest: boolean = false, instructor: boolean = false): Observable<Feedback> {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/feedback`;
    if (latest || instructor) {
      let searchParams = new URLSearchParams({
        "instructor-version": String(instructor),
        "latest": String(latest)
      })
      url += '?' + searchParams;
    }
    return request<Feedback>(HTTPMethod.GET, url)
  }

  export function getProperties(lectureId: number, assignmentId: number, submissionId: number): Observable<object> {
    let url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}/properties`;
    return request<object>(HTTPMethod.GET, url);
  }

  export function updateProperties(lectureId: number, assignmentId: number, submissionId: number, properties: object): Observable<Submission> {
    let url = `/lectures/${lectureId}/assignments/${assignmentId}/submissions/${submissionId}/properties`;
    return request<Submission>(HTTPMethod.PUT, url, properties);
  }