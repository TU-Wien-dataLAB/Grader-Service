import { Observable, from } from 'rxjs';
import { switchMap } from 'rxjs/operators'

export enum HTTPMethod {
  GET="GET", POST="POST", PUT="PUT", DELETE="DELETE"
}

export interface RequestOptions {
  method: HTTPMethod,
  mode: string,
  headers: object
  body: object
}

export function request<T>(url: string, options: RequestInit): Observable<T> {
  return from(fetch(url, options)).pipe(
    switchMap(response => response.json())
  )
}