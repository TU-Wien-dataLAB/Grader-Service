import * as React from 'react';
import {
  Card, IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Paper, Typography
} from '@mui/material';
import InsertDriveFileRoundedIcon from '@mui/icons-material/InsertDriveFileRounded';
import {FilterFileBrowserModel} from '@jupyterlab/filebrowser/lib/model';
import {GlobalObjects} from '../../index';
import {Contents} from '@jupyterlab/services';
import IModel = Contents.IModel;
import {SxProps} from "@mui/system";
import {Theme} from "@mui/material/styles";
import {Submission} from "../../model/submission";
import ChatRoundedIcon from "@mui/icons-material/ChatRounded";
import {utcToLocalFormat} from "../../services/datetime.service";
import CloudDoneRoundedIcon from "@mui/icons-material/CloudDoneRounded";

interface ISubmissionListProps {
  submissions: Submission[];
  sx?: SxProps<Theme>;
}

export const SubmissionList = (props: ISubmissionListProps) => {

  const openFeedback = async (submission: Submission) => {
    console.log('Opening Feedback for Submission: ' + submission.id);

  };

  // generateItems will be fed using the IIterator from the FilterFileBrowserModel
  const generateItems = (submissions: Submission[]) => {
    return submissions.reverse().map(value => (
      <ListItem disablePadding
                secondaryAction={
                  value.feedback_available
                    ? <IconButton edge="end" aria-label="delete" onClick={() => openFeedback(value)}>
                      <ChatRoundedIcon/>
                    </IconButton>
                    : null
                }>
        <ListItemIcon>
          <CloudDoneRoundedIcon sx={{ml: 1}}/>
        </ListItemIcon>
        <ListItemText primary={utcToLocalFormat(value.submitted_at)}/>
      </ListItem>
    ));
  };

  return (
    <Paper elevation={0} sx={props.sx}>
      <Card sx={{mt: 1}} variant="outlined">
        {props.submissions.length === 0
          ? <Typography variant={'body1'} sx={{ml: 1}}>No Submissions Yet</Typography>
          : <List dense={true}>{generateItems(props.submissions)}</List>
        }
      </Card>
    </Paper>
  );
};
