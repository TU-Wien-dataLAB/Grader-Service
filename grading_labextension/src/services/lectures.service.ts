import { Lecture } from '../model/lecture';
import { request, HTTPMethod } from './request.service';

export function createLecture(lecture: Lecture): Promise<Lecture> {
  return request<Lecture>(HTTPMethod.POST, '/lectures', lecture);
}

export function getAllLectures(): Promise<Lecture[]> {
  return request<Lecture[]>(HTTPMethod.GET, '/lectures');
}

export function updateLecture(lecture: Lecture): Promise<Lecture> {
  return request<Lecture>(HTTPMethod.PUT, `/lectures/${lecture.id}`, lecture);
}

export function getLecture(lectureId: number): Promise<Lecture> {
  return request<Lecture>(HTTPMethod.GET, `/lectures/${lectureId}`);
}

export function deleteLecture(lectureId: number): void {
  request<void>(HTTPMethod.DELETE, `/lectures/${lectureId}`);
}

//TODO: create Datapackage model to replace any
export function getUsers(lecture: Lecture) : Promise<any> {
  return request<any>(HTTPMethod.GET, `/lectures/${lecture.id}/users`);
}
