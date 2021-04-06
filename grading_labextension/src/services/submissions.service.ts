import { Observable } from "rxjs";
import { Assignment } from "../model/assignment";
import { Feedback } from "../model/feedback";
import { Lecture } from "../model/lecture";
import { Submission } from "../model/submission";
import { request, HTTPMethod } from "./request.service";


export function submitAssignment(lecture: Lecture, assignement : Assignment): Observable<void> {
    return request<void>(HTTPMethod.POST, `/lectures/${lecture.id}/assignments/${assignement.id}/submissions`, {}, {})
  }


export function getAllSubmissions(lecture: Lecture, assignement : Assignment): Observable<Submission[]> {
    return request<Submission[]>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignement.id}/submissions`, {})
  }

  export function getFeedback(lecture: Lecture, assignement : Assignment): Observable<Feedback> {
    return request<Feedback>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignement.id}/feedback`, {})
  }