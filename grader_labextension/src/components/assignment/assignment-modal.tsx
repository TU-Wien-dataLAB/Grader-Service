import * as React from 'react';
import { Lecture } from '../../model/lecture';
import { Assignment } from '../../model/assignment';
import { Submission } from '../../model/submission';
import { ModalTitle } from '../util/modal-title';
import { Box, Typography } from '@mui/material';
import { SubmissionList } from './submission-list';
import LoadingOverlay from '../util/overlay';
import { Feedback } from './feedback';
import { AssignmentStatus } from './assignment-status';
import { AssignmentFilesComponent } from './assignment-files';

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
  };

  return (
    <div style={{ overflow: 'scroll', height: '100%' }}>
      <ModalTitle title={props.assignment.name} />
      <Box sx={{ mt: 10 }}>
        <Typography variant={'h6'} sx={{ ml: 2 }}>
          Status
        </Typography>
        <AssignmentStatus
          lecture={props.lecture}
          assignment={props.assignment}
          submissions={submissions}
        />

        <Typography variant={'h6'} sx={{ ml: 2 }}>
          Files
        </Typography>
        <AssignmentFilesComponent
          lecture={props.lecture}
          assignment={props.assignment}
          showAlert={props.showAlert}
          setSubmissions={setSubmissions}
        />

        <Typography variant={'h6'} sx={{ ml: 2, mt: 3 }}>
          Submissions
        </Typography>
        <SubmissionList
          submissions={submissions}
          openFeedback={openFeedback}
          sx={{ m: 2, mt: 1 }}
        />
      </Box>
      <LoadingOverlay
        onClose={() => setShowFeedback(false)}
        open={showFeedback}
        container={props.root}
      >
        <Feedback
          lecture={props.lecture}
          assignment={props.assignment}
          submission={feedbackSubmission}
          showAlert={props.showAlert}
        />
      </LoadingOverlay>
    </div>
  );
};
