import * as React from 'react';
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  Chip,
  Stack,
  Typography
} from '@mui/material';

import ChatRoundedIcon from '@mui/icons-material/ChatRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';
import ReportRoundedIcon from '@mui/icons-material/ReportRounded';

import { Assignment } from '../../model/assignment';
import LoadingOverlay from '../util/overlay';
import { Lecture } from '../../model/lecture';
import { getAllSubmissions } from '../../services/submissions.service';
import { getAssignment } from '../../services/assignments.service';
import { DeadlineComponent } from '../util/deadline';
import { AssignmentModalComponent } from './assignment-modal';
import { Submission } from '../../model/submission';
import { User } from '../../model/user';

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const [displayAssignment, setDisplayAssignment] = React.useState(false);
  const [submissions, setSubmissions] = React.useState([] as Submission[]);
  React.useEffect(() => {
    getAllSubmissions(props.lecture, assignment, false, false).then(
      response => {
        setSubmissions(response[0].submissions);
      }
    );
  }, [props]);

  const onAssignmentClose = async () => {
    setDisplayAssignment(false);
    setAssignment(await getAssignment(props.lecture.id, assignment));
    const submissions = await getAllSubmissions(props.lecture, assignment, false, false);
    setSubmissions(submissions[0].submissions);
  };

  return (
    <Box>
      <Card
        sx={{ maxWidth: 225, minWidth: 225, m: 1.5 }}
        onClick={e => setDisplayAssignment(true)}
      >
        <CardActionArea>
          <CardContent>
            <Typography variant="h5" component="div">
              {assignment.name}
            </Typography>

            <Stack sx={{ display: 'flex', flexDirection: 'column' }}>
              <DeadlineComponent
                sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                due_date={assignment.due_date}
                compact={true}
              />
              <Chip
                sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                size="small"
                icon={<CloudDoneRoundedIcon />}
                label={'Submissions: ' + submissions.length}
              />
              <Chip
                sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                size="small"
                icon={<ChatRoundedIcon />}
                label={
                  'Feedback available: ' +
                  submissions.reduce(
                    (accum: boolean, curr: Submission) =>
                      accum || curr.feedback_available,
                    false
                  )
                }
              />
              {assignment.status === 'released' ? null : (
                <Chip
                  sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                  size="small"
                  icon={<ReportRoundedIcon />}
                  label="Not Released"
                  color="error"
                />
              )}
            </Stack>
          </CardContent>
        </CardActionArea>
      </Card>
      <LoadingOverlay
        onClose={onAssignmentClose}
        open={displayAssignment}
        container={props.root}
        transition="zoom"
      >
        <AssignmentModalComponent
          lecture={props.lecture}
          assignment={assignment}
          submissions={submissions}
        />
      </LoadingOverlay>
    </Box>
  );
};
