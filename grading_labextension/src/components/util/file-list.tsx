import * as React from 'react';
import {
  Card,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper
} from '@mui/material';
import InsertDriveFileRoundedIcon from '@mui/icons-material/InsertDriveFileRounded';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { GlobalObjects } from '../../index';
import { Contents } from '@jupyterlab/services';
import IModel = Contents.IModel;

interface IFileListProps {
  path: string;
}

export const FilesList = (props: IFileListProps) => {
  const [files, setFiles] = React.useState([]);

  const openFile = (path: string) => {
    console.log(path);
  };

  const model = new FilterFileBrowserModel({
    auto: true,
    manager: GlobalObjects.docManager
  });

  const getFiles = async () => {
    await model.cd(props.path);
    const items = model.items();
    const files = [];
    let f: IModel = items.next();
    while (f !== undefined) {
      files.push(f);
      f = items.next();
    }
    setFiles(files);
  };

  // generateItems will be fed using the IIterator from the FilterFileBrowserModel
  const generateItems = (files: IModel[]) => {
    return files.map(value => (
      <ListItem disablePadding>
        <ListItemButton onDoubleClick={() => openFile(value.path)} dense={true}>
          <ListItemIcon>
            <InsertDriveFileRoundedIcon />
          </ListItemIcon>
          <ListItemText primary={value.path} />
        </ListItemButton>
      </ListItem>
    ));
  };

  getFiles();

  return (
    <Paper elevation={0}>
      <Card sx={{ mt: 1 }} variant="outlined">
        <List dense={true}>{generateItems(files)}</List>
      </Card>
    </Paper>
  );
};
