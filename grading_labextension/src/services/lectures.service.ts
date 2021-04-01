import { Observable } from 'rxjs';
import { Lecture } from '../model/lecture';
import {request, HTTPMethod} from './request.service'

export function createLecture(lecture: Lecture): Observable<Lecture> {
  return request<Lecture>(HTTPMethod.POST, "/lectures", {}, lecture)
}

export function getAllLectures(): Observable<Lecture[]> {
  return request<Lecture[]>(HTTPMethod.GET, "/lectures", {})
}

export function updateLecture(lecture: Lecture): Observable<Lecture> {
  return request<Lecture>(HTTPMethod.PUT, `/lectures/${lecture.id}`, {}, lecture)
}

export function getLecture(lectureId: number): Observable<Lecture> {
  return request<Lecture>(HTTPMethod.GET, `/lectures/${lectureId}`, {})
}

export function deleteLecture(lectureId: number): void {
  request<void>(HTTPMethod.DELETE, `/lectures/${lectureId}`, {})
}
