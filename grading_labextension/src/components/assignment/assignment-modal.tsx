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
import {pullAssignment} from "../../services/assignments.service";
import {getAllSubmissions, getSubmissions, submitAssignment} from "../../services/submissions.service";

export interface IAssignmentModalProps {
  lecture: Lecture;
  assignment: Assignment;
  submissions: Submission[];
}

export const AssignmentModalComponent = (props: IAssignmentModalProps) => {
  const [submissions, setSubmissions] = React.useState(props.submissions);
  const [path, setPath] = React.useState(`${props.lecture.code}/${props.assignment.name}`);
  const [alert, setAlert] = React.useState(false);
  const [severity, setSeverity] = React.useState('success');
  const [alertMessage, setAlertMessage] = React.useState('');

  const showAlert = (severity: string, msg: string) => {
    setSeverity(severity);
    setAlertMessage(msg);
    setAlert(true);
  };

  const handleAlertClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === 'clickaway') {
      return;
    }
    setAlert(false);
  };

  const fetchAssignmentHandler = async (repo: "user" | "release") => {
    try {
      await pullAssignment(props.lecture.id, props.assignment.id, repo);
      showAlert('success', 'Successfully Pulled Repo');
    } catch (e) {
      showAlert('error', 'Error Fetching Assignment');
    }
  }

  const submitAssignmentHandler = async () => {
    try {
      await submitAssignment(props.lecture, props.assignment);
    } catch (e) {
      showAlert('error', 'Error Submitting Assignment');
    }
    try {
      const submissions = await getAllSubmissions(props.lecture, props.assignment, false, false);
      setSubmissions(submissions[0].submissions)
    } catch (e) {
      showAlert('error', 'Error Updating Submissions');
    }
  }

  return (
    <Box>
      <ModalTitle title={props.assignment.name}/>
      <Typography variant={'h6'} sx={{ml: 2}}>Files</Typography>
      <FilesList path={path} sx={{m: 2, mt: 1}}/>
      <Stack direction={"row"} spacing={1} sx={{m: 1, ml: 2}}>
        <Button
          variant="outlined"
          size="small"
          onClick={() => submitAssignmentHandler()}
        >
          <PublishRoundedIcon fontSize="small" sx={{mr: 1}}/>
          Submit
        </Button>
        <SplitButton
          variant="outlined"
          size="small"
          icon={<GetAppRoundedIcon fontSize="small" sx={{mr: 1}}/>}
          options={[
            {name: "Pull User", onClick: () => fetchAssignmentHandler("user")},
            {name: "Pull Release", onClick: () => fetchAssignmentHandler("release")}
          ]}
        />
      </Stack>
      <Typography variant={'h6'} sx={{ml: 2, mt: 3}}>Submissions</Typography>
      <SubmissionList submissions={submissions} sx={{m: 2, mt: 1}}/>


      <Portal container={document.body}>
        <Snackbar
          open={alert}
          autoHideDuration={3000}
          onClose={handleAlertClose}
          sx={{mb: 2, ml: 2}}
        >
          <MuiAlert
            onClose={handleAlertClose}
            severity={severity as AlertProps['severity']}
            sx={{width: '100%'}}
          >
            {alertMessage}
          </MuiAlert>
        </Snackbar>
      </Portal>
    </Box>
  );
};
