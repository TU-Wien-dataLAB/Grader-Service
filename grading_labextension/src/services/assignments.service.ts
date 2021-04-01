import { Observable } from 'rxjs';
import { Assignment } from '../model/assignment';
import {request, HTTPMethod} from './request.service'

export function createAssignment(lectureId: number, assignment: Assignment): Observable<Assignment> {
  return request<Assignment>(HTTPMethod.POST, `/lectures/${lectureId}/assignments`, {}, assignment)
}

export function getAllAssignments(lectureId: number): Observable<Assignment[]> {
  return request<Assignment[]>(HTTPMethod.GET, `/lectures/${lectureId}/assignments`, {})
}

export function updateAssignment(lectureId: number, assignment: Assignment): Observable<Assignment> {
  return request<Assignment>(HTTPMethod.PUT, `/lectures/${lectureId}/assignments/${assignment.id}`, {}, assignment)
}

export function getAssignment(lectureId: number, assignmentId: number): Observable<Assignment> {
  return request<Assignment>(HTTPMethod.GET, `/lectures/${lectureId}/assignments/${assignmentId}`, {})
}

export function deleteAssignment(lectureId: number, assignmentId: number): void {
  request<void>(HTTPMethod.DELETE, `/lectures/${lectureId}/assignments/${assignmentId}`, {})
}
