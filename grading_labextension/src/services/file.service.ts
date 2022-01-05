import {FilterFileBrowserModel} from "@jupyterlab/filebrowser/lib/model";
import {GlobalObjects} from "../index";
import {Contents} from '@jupyterlab/services';
import IModel = Contents.IModel;

export const getFiles = async (path: string): Promise<IModel[]> => {
  const model = new FilterFileBrowserModel({
    auto: true,
    manager: GlobalObjects.docManager
  });
  await model.cd(path);
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