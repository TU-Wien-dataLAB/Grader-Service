import {FilterFileBrowserModel} from "@jupyterlab/filebrowser/lib/model";
import {GlobalObjects} from "../index";
import {Contents} from '@jupyterlab/services';
import IModel = Contents.IModel;
import {Assignment} from "../model/assignment";
import {HTTPMethod, request} from "./request.service";
import {Lecture} from "../model/lecture";
import { RepoType } from "../components/util/repo-type";

export const getFiles = async (path: string): Promise<IModel[]> => {
  if (path === null) return [];
  const model = new FilterFileBrowserModel({
    auto: true,
    manager: GlobalObjects.docManager
  });
  try {
    await model.cd(path);
  } catch (_) {
    return [];
  }

  if (model.path !== path) {
    return [];
  }
  const items = model.items();
  const files = [];
  let f: IModel = items.next();
  while (f !== undefined) {
    files.push(f);
    f = items.next();
  }
  console.log('getting files from path ' + path);
  return files;
};

export interface IGitLogObject {
  commit: string,
  author: string,
  date: string,
  ref: string,
  commit_msg: string,
  pre_commit: string
}

export function getGitLog(lecture: Lecture, assignment: Assignment, repo: RepoType, nCommits: number): Promise<IGitLogObject[]> {
  let url = `/lectures/${lecture.id}/assignments/${assignment.id}/log/${repo}/`;
  let searchParams = new URLSearchParams({
    "n": String(nCommits)
  })
  url += '?' + searchParams;
  return request<IGitLogObject[]>(HTTPMethod.GET, url);
}