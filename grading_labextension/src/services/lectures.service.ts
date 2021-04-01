import { Observable } from 'rxjs';
import { Lecture } from '../model/lecture';
import {request} from './request.service'

export function getAllLectures(): Observable<Lecture[]> {
  return request<Lecture[]>("/lectures", {})
}