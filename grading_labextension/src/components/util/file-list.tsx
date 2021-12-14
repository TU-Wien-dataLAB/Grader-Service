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

  React.useEffect(() => {
    getFiles().then(files => setFiles(files));
  }, []);

  const openFile = async (path: string) => {
    console.log('Opening file: ' + path);
    GlobalObjects.commands
      .execute('docmanager:open', {
        path: path,
        options: {
          mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
        }
      })
      .catch(error => {
        // TODO: refactor showAlert to work in all components
        // showAlert('error', 'Error Opening File');
        console.log(error);
      });
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
    console.log('getting files from path ' + props.path);
    return files;
  };

  // generateItems will be fed using the IIterator from the FilterFileBrowserModel
  const generateItems = (files: IModel[]) => {
    return files.map(value => (
      <ListItem disablePadding>
        <ListItemButton onDoubleClick={() => openFile(value.path)} dense={true}>
          <ListItemIcon>
            <InsertDriveFileRoundedIcon />
          </ListItemIcon>
          <ListItemText primary={value.name} />
        </ListItemButton>
      </ListItem>
    ));
  };

  return (
    <Paper elevation={0}>
      <Card sx={{ mt: 1 }} variant="outlined">
        <List dense={true}>{generateItems(files)}</List>
      </Card>
    </Paper>
  );
};
