import { Observable } from 'rxjs';
import { Assignment } from '../model/assignment';
import { request, HTTPMethod } from './request.service'

export function createAssignment(lectureId: number, assignment: Assignment): Observable<Assignment> {
  return request<Assignment>(HTTPMethod.POST, `/lectures/${lectureId}/assignments`, assignment)
}

export function getAllAssignments(lectureId: number): Observable<Assignment[]> {
  return request<Assignment[]>(HTTPMethod.GET, `/lectures/${lectureId}/assignments`)
}

export function updateAssignment(lectureId: number, assignment: Assignment): Observable<Assignment> {
  return request<Assignment>(HTTPMethod.PUT, `/lectures/${lectureId}/assignments/${assignment.id}`, assignment)
}

export function fetchAssignment(lectureId: number, assignmentId: number, instructor: boolean = false, metadataOnly: boolean = false): Observable<Assignment> {
  let url = `/lectures/${lectureId}/assignments/${assignmentId}`;
  if (instructor || metadataOnly) {
    let searchParams = new URLSearchParams({
      "instructor-version": String(instructor),
      "metadata-only": String(metadataOnly)
    })
    url += '?' + searchParams;
  }

  return request<Assignment>(HTTPMethod.GET, url)
}

export function deleteAssignment(lectureId: number, assignmentId: number): void {
  request<void>(HTTPMethod.DELETE, `/lectures/${lectureId}/assignments/${assignmentId}`)
}
