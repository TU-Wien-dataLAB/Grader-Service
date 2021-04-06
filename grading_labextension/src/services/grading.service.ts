import { Observable } from 'rxjs';
import { Lecture } from '../model/lecture';
import { Assignment } from '../model/assignment'
import {User} from '../model/user'
import {ManualGradingContent} from '../model/manualGradingContent'
import {GradingResult} from '../model/gradingResult'
import {request, HTTPMethod} from './request.service'
import { Feedback } from '../model/feedback';

export function createManualFeedback(lecture: Lecture, assignment : Assignment, student: User, manual: ManualGradingContent): Observable<Feedback> {
    return request<Feedback>(HTTPMethod.POST, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.id}/manual`, {}, manual)
  }

export function autogradeSubmission(lecture: Lecture, assignment : Assignment, student: User): Observable<Assignment> {
    return request<Assignment>(HTTPMethod.POST, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.id}/auto`, {}, student)
  }

  //response is not a schema => any
  //should prob be changed
export function getStudentSubmissions(lecture: Lecture, assignment : Assignment): Observable<any> {
    return request<any>(HTTPMethod.GET, `/lectures/${lecture.id}/assignements/${assignment.id}/grading`, {})
  }

export function getManualFeedback(lecture: Lecture, assignement : Assignment, student: User): Observable<ManualGradingContent> {
    return request<ManualGradingContent>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignement.id}/grading/${student.id}/manual`, {})
  }


export function updateManualFeedback(lecture: Lecture, assignement : Assignment, student: User, manual: ManualGradingContent): Observable<ManualGradingContent> {
    return request<ManualGradingContent>(HTTPMethod.PUT, `/lectures/${lecture.id}/assignements/${assignement.id}/grading/${student.id}/manual`, {}, manual)
  }


export function deleteManualFeedback(lecture: Lecture, assignment : Assignment, student: User, manual: ManualGradingContent): Observable<any> {
    return request<any>(HTTPMethod.DELETE, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.id}/manual`, {}, manual)
  }

export function getGrade(lecture: Lecture, assignment : Assignment, student: User): Observable<GradingResult> {
    return request<GradingResult>(HTTPMethod.GET, `/lectures/${lecture.id}/assignments/${assignment.id}/grading/${student.id}/score`, {})
  }






