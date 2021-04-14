import { Observable } from "rxjs";
import { map } from "rxjs/operators";
import { Assignment } from "../model/assignment";
import { Feedback } from "../model/feedback";
import { Lecture } from "../model/lecture";
import { UserSubmissions } from "../model/userSubmissions";
import { request, HTTPMethod } from "./request.service";


  export function submitAssignment(lecture: Lecture, assignment : Assignment): Observable<void> {
    return request<void>(HTTPMethod.POST, `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`, {}, {})
  }

  export function getSubmissions(lecture: Lecture, assignment : Assignment, latest: boolean = false): Observable<UserSubmissions> {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;
    if (latest) {
      let searchParams = new URLSearchParams({
        "latest": String(latest)
      })
      url += '?' + searchParams;
    }
    return request<UserSubmissions[]>(HTTPMethod.GET, url, {}).pipe(map(array => array[0]))
  }

  export function getAllSubmissions(lecture: Lecture, assignment : Assignment, latest: boolean = false, instructor: boolean = true): Observable<UserSubmissions[]> {
    let url = `/lectures/${lecture.id}/assignments/${assignment.id}/submissions`;

    if (latest || instructor) {
      let searchParams = new URLSearchParams({
        "instructor-version": String(instructor),
        "latest": String(latest)
      })
      url += '?' + searchParams;
    }
    return request<UserSubmissions[]>(HTTPMethod.GET, url, {})

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
    return request<Feedback>(HTTPMethod.GET, url, {})
  }