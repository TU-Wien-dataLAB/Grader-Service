import * as React from 'react';
import {Lecture} from '../../model/lecture';
import {Assignment} from '../../model/assignment';
import {Submission} from '../../model/submission';
import {ModalTitle} from '../util/modal-title';
import {AlertProps, Box, Button, Portal, Snackbar, Stack, Typography} from '@mui/material';
import {FilesList} from "../util/file-list";
import PublishRoundedIcon from "@mui/icons-material/PublishRounded";
import GetAppRoundedIcon from "@mui/icons-material/GetAppRounded";
import {SplitButton} from "../util/split-button";
import MuiAlert from "@mui/material/Alert";
import {SubmissionList} from "./submission-list";
import {pullAssignment, pushAssignment, resetAssignment} from "../../services/assignments.service";
import {getAllSubmissions, getSubmissions, submitAssignment} from "../../services/submissions.service";
import LoadingOverlay from "../util/overlay";
import {Feedback} from "./feedback";
import {AssignmentStatus} from "./assignment-status";
import {getFiles} from "../../services/file.service";
import { AgreeDialog } from '../coursemanage/dialog';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import GradingIcon from '@mui/icons-material/Grading';
import { RepoType } from '../util/repo-type';
import { AssignmentControlComponent } from './assignment-control';

export interface IAssignmentModalProps {
  lecture: Lecture;
  assignment: Assignment;
  submissions: Submission[];
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
}

export const AssignmentModalComponent = (props: IAssignmentModalProps) => {
  const [submissions, setSubmissions] = React.useState(props.submissions);
  const [showFeedback, setShowFeedback] = React.useState(false);
  const [feedbackSubmission, setFeedbackSubmission] = React.useState(null);

  const openFeedback = (submission: Submission) => {
    setFeedbackSubmission(submission);
    setShowFeedback(true);
  }

  
  return (
    <div style={{overflow: "scroll", height: "100%"}}>
      <ModalTitle title={props.assignment.name}/>
      <Box sx={{mt: 10}}>
        <Typography variant={'h6'} sx={{ml: 2}}>Status</Typography>
        <AssignmentStatus lecture={props.lecture} assignment={props.assignment} submissions={submissions}/>
        
        <Typography variant={'h6'} sx={{ml: 2}}>Files</Typography>
        <AssignmentControlComponent lecture={props.lecture} assignment={props.assignment} showAlert={props.showAlert} setSubmissions={setSubmissions}/>

        <Typography variant={'h6'} sx={{ml: 2, mt: 3}}>Submissions</Typography>
        <SubmissionList submissions={submissions} openFeedback={openFeedback} sx={{m: 2, mt: 1}}/>

      </Box>
      <LoadingOverlay onClose={() => setShowFeedback(false)} open={showFeedback} container={props.root}>
        <Feedback lecture={props.lecture} assignment={props.assignment} submission={feedbackSubmission}
                  showAlert={props.showAlert}/>
      </LoadingOverlay>      
    </div>
    
  );
};
