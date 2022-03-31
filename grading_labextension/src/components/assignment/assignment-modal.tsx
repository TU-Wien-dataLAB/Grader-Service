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
import { RepoType } from '../util/repo-type';

export interface IAssignmentModalProps {
  lecture: Lecture;
  assignment: Assignment;
  submissions: Submission[];
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
}

export const AssignmentModalComponent = (props: IAssignmentModalProps) => {
  const [submissions, setSubmissions] = React.useState(props.submissions);
  const [path, setPath] = React.useState(`${props.lecture.code}/${props.assignment.name}`);
  const [showFeedback, setShowFeedback] = React.useState(false);
  const [feedbackSubmission, setFeedbackSubmission] = React.useState(null);
  const [hasFiles, setHasFiles] = React.useState(false);
  const [dialog, setDialog] = React.useState(false);

  React.useEffect(() => {
    getFiles(path).then(files => setHasFiles(files.length > 0));
  }, [props]);

  const fetchAssignmentHandler = async (repo: "user" | "release") => {
    try {
      await pullAssignment(props.lecture.id, props.assignment.id, repo);
      props.showAlert('success', 'Successfully Pulled Repo');
    } catch (e) {
      props.showAlert('error', 'Error Fetching Assignment');
    }
  }

  const resetAssignmentHandler = async () => {
    //await pushAssignment(props.lecture.id, props.assignment.id, RepoType.ASSIGNMENT, "Commit before reset");
    try {
      await resetAssignment(props.lecture,props.assignment).then( () => fetchAssignmentHandler("user"));
      props.showAlert('success', 'Successfully Reset Assignment');
    } catch (e) {
      props.showAlert('error', 'Error Reseting Assignment');
    }
    setDialog(false);
  }

  const submitAssignmentHandler = async () => {
    try {
      await submitAssignment(props.lecture, props.assignment);
      props.showAlert('success', 'Successfully Submitted Assignment');
    } catch (e) {
      props.showAlert('error', 'Error Submitting Assignment');
    }
    try {
      const submissions = await getAllSubmissions(props.lecture, props.assignment, false, false);
      setSubmissions(submissions)
    } catch (e) {
      props.showAlert('error', 'Error Updating Submissions');
    }
  }

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
        <FilesList path={path} showAlert={props.showAlert} sx={{m: 2, mt: 1}}/>
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
            selectedIndex={hasFiles ? 0 : 1}
          />
          <Button
            variant="outlined"
            size="small"
            color="error"
            onClick={() => setDialog(true)}
          >
            <RestartAltIcon fontSize="small" sx={{mr: 1}}/>
            Reset
          </Button>
        </Stack>

        <Typography variant={'h6'} sx={{ml: 2, mt: 3}}>Submissions</Typography>
        <SubmissionList submissions={submissions} openFeedback={openFeedback} sx={{m: 2, mt: 1}}/>

      </Box>
      <LoadingOverlay onClose={() => setShowFeedback(false)} open={showFeedback} container={props.root}>
        <Feedback lecture={props.lecture} assignment={props.assignment} submission={feedbackSubmission}
                  showAlert={props.showAlert}/>
      </LoadingOverlay>
      {/* AgreeDialog for assignment reset */}
      <AgreeDialog 
      open={dialog} 
      title={'Reset Assignment'} 
      message={'This action will delete your current progress and reset the assignment! \n' +
      'Therefore you should copy and paste your work to a different directory before progressing. '} 
      handleAgree={resetAssignmentHandler} 
      handleDisagree={() => setDialog(false)} />
    </div>
    
  );
};
