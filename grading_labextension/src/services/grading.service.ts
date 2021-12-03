import { Observable } from 'rxjs';
import { Lecture } from '../model/lecture';
import { Assignment } from '../model/assignment'
import { User } from '../model/user'
import { request, HTTPMethod } from './request.service'
import { Submission } from '../model/submission';

export function createManualFeedback(lectid: number, assignid: number, subid: number): Observable<any> {
  return request<any>(HTTPMethod.GET, `/lectures/${lectid}/assignments/${assignid}/grading/${subid}/manual`)
}

export function autogradeSubmission(lecture: Lecture, assignment: Assignment, submission: Submission): Observable<any> {
  return request<Assignment>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${submission.id}/auto`)
}

export function generateFeedback(lecture_id: number, assignment_id: number, submission_id: number): Observable<Submission> {
  return request<Submission>(HTTPMethod.GET, `/lectures/${lecture_id}/assignments/${assignment_id}/grading/${submission_id}/feedback`)
}

//response is not a schema => any
//TODO: should prob be changed
export function getStudentSubmissions(lecture: Lecture, assignment: Assignment): Observable<any> {
  return request<any>(HTTPMethod.GET, `/lectures/${lecture.id}/assignements/${assignment.id}/grading`)
}

export function getManualFeedback(lecture: Lecture, assignment: Assignment, student: User): Observable<object> {
  return request<object>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.name}/manual`)
}


export function updateManualFeedback(lecture: Lecture, assignment: Assignment, student: User, manual: object): Observable<object> {
  return request<object>(HTTPMethod.PUT, `/lectures/${lecture.id}/assignements/${assignment.id}/grading/${student.name}/manual`, manual)
}


export function deleteManualFeedback(lecture: Lecture, assignment: Assignment, student: User, manual: object): Observable<any> {
  return request<any>(HTTPMethod.DELETE, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.name}/manual`, manual)
}

export function getGrade(lecture: Lecture, assignment: Assignment, student: User): Observable<object> {
  return request<object>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.name}/score`)
}






