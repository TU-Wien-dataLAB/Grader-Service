import * as React from 'react';
import {
  Card,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper, Typography
} from '@mui/material';
import InsertDriveFileRoundedIcon from '@mui/icons-material/InsertDriveFileRounded';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { GlobalObjects } from '../../index';
import { Contents } from '@jupyterlab/services';
import IModel = Contents.IModel;
import {SxProps} from "@mui/system";
import {Theme} from "@mui/material/styles";
import {getFiles} from "../../services/file.service";

interface IFileListProps {
  path: string;
  reloadFiles?: boolean;
  sx?: SxProps<Theme>;
}

export const FilesList = (props: IFileListProps) => {
  const [files, setFiles] = React.useState([]);

  React.useEffect(() => {
    getFiles(props.path).then(files => setFiles(files));
  }, [props]);

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
    <Paper elevation={0} sx={props.sx}>
      <Card sx={{ mt: 1, height: '80%' }} variant="outlined">
        {files.length === 0
          ? <Typography variant={'body1'} sx={{ml: 1}}>No Files Found</Typography>
          : <List dense={false}>{generateItems(files)}</List>
        }
      </Card>
    </Paper>
  );
};
