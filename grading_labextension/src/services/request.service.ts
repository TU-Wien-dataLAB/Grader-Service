import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { Observable, from } from 'rxjs';
import { switchMap } from 'rxjs/operators'

export enum HTTPMethod {
  GET="GET", POST="POST", PUT="PUT", DELETE="DELETE"
}

export function request<T>(method: HTTPMethod, endPoint: string, options: RequestInit, body: object = null,  url: string = "http://128.130.202.214:8000/services/mock"): Observable<T> {
  options.method = method
  if (body) {
    options.body = JSON.stringify(body)
  }

  const settings = ServerConnection.makeSettings();
  let requestUrl = "";
  if (url == null) {
    // ServerConnection only allows requests to notebook baseUrl
    requestUrl = URLExt.join(
      settings.baseUrl,
      "/grading_labextension", // API Namespace
      endPoint
    );

    console.log("Request " + method.toString() + " URL: " + requestUrl)
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
      "Authorization": "Bearer 123"
    }
    console.log("Request " + method.toString() + " URL: " + requestUrl)
    return from(fetch(requestUrl, options)).pipe(
      switchMap(async response => {
        let data: any = await response.json();
        return data
      })
    )
  }

}