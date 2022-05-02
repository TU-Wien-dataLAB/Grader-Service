import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { from, throwError } from 'rxjs';
import { switchMap } from 'rxjs/operators'

export enum HTTPMethod {
  GET = "GET", POST = "POST", PUT = "PUT", DELETE = "DELETE"
}

export function request<T>(method: HTTPMethod, endPoint: string, body: object = null, headers: HeadersInit = null): Promise<T> {
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
    "/grader_labextension", // API Namespace
    endPoint
  );

  return from(ServerConnection.makeRequest(requestUrl, options, settings)).pipe(
    switchMap(async response => {
      if(response.status != 200) {
        throw throwError(await response.text())
      }
      console.log(response)
      let data: any = await response.text();
      if (data.length > 0) {
        try {
          data = JSON.parse(data);
        } catch (error) {
          console.log('Not a JSON response body.', response);
        }
      }
      console.log("Request " + method.toString() + " URL: " + requestUrl);
      console.log(data)
      return data
    })
  ).toPromise()

}