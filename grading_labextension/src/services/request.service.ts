import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { Observable, from } from 'rxjs';
import { switchMap } from 'rxjs/operators'

export enum HTTPMethod {
  GET = "GET", POST = "POST", PUT = "PUT", DELETE = "DELETE"
}

export interface RequestOptions {
  method: HTTPMethod,
  mode: string,
  headers: object
  body: object
}

export function request<T>(endPoint: string, options: RequestInit, url: string = "128.130.202.214:8000"): Observable<T> {
  const settings = ServerConnection.makeSettings();
  let requestUrl: string = "";
  if (url == null) {
    requestUrl = URLExt.join(
      settings.baseUrl,
      'grading_labextension', // API Namespace
      endPoint
    );
    console.log("Request URL:" + requestUrl)
    return from(ServerConnection.makeRequest(requestUrl, options, settings)).pipe(
      switchMap(async response => {
        let data: any = await response.text();

        if (data.length > 0) {
          try {
            data = JSON.parse(data);
          } catch (error) {
            console.log('Not a JSON response body.', response);
          }
        }

        return data
      })
    )
  } else {
    requestUrl = url + endPoint
    options.headers = {
      'Authorization': 'Bearer 0b79bab50daca910b000d4f1a2b675d604257e42'
    },
    console.log("Request URL:" + requestUrl)
    console.log("We are in mocking api ;))))))")
    return from(fetch(requestUrl, options)).pipe(
      switchMap(async response => {
        console.log(response);
        let data: any = await response.json()
        console.log(data)

        return data
      })
    )
  }

}