import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { Observable, from } from 'rxjs';
import { switchMap } from 'rxjs/operators'

export enum HTTPMethod {
  GET = "GET", POST = "POST", PUT = "PUT", DELETE = "DELETE"
}

export function request<T>(method: HTTPMethod, endPoint: string, body: object = null, headers: HeadersInit = null): Observable<T> {
  let options: RequestInit = {}
  options.method = method
  if (body) {
    options.body = JSON.stringify(body)
  }
  if (headers) {
    options.headers = headers
  }
  const settings = ServerConnection.makeSettings();
  let requestUrl = "";

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

}