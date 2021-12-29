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

import AccessAlarmRoundedIcon from '@mui/icons-material/AccessAlarmRounded';
import AssignmentTurnedInRoundedIcon from '@mui/icons-material/AssignmentTurnedInRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';

import { Assignment } from '../../model/assignment';
import LoadingOverlay from '../util/overlay';
import { Lecture } from '../../model/lecture';
import { getAllSubmissions } from '../../services/submissions.service';
import { AssignmentModalComponent } from './assignment-modal';
import { DeadlineComponent } from '../util/deadline';

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [displaySubmissions, setDisplaySubmissions] = React.useState(false);
  const onSubmissionClose = () => setDisplaySubmissions(false);

  const [latestSubmissions, setSubmissions] = React.useState([]);
  React.useEffect(() => {
    getAllSubmissions(props.lecture, props.assignment, true, true).then(
      (response: any) => {
        setSubmissions(response);
      }
    );
  }, [props]);

  return (
    <Card elevation={5} sx={{ maxWidth: 225, minWidth: 225, m: 1.5 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {props.assignment.name}
        </Typography>

        <Stack sx={{ display: 'flex', flexDirection: 'column' }}>
          <DeadlineComponent
            sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
            due_date={props.assignment.due_date}
            compact={true}
          />
          <Chip
            sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
            size="small"
            icon={<AssignmentTurnedInRoundedIcon />}
            label={props.assignment.status}
          />
          <Chip
            sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
            size="small"
            icon={<CloudDoneRoundedIcon />}
            label={'Submissions: ' + latestSubmissions.length}
          />
        </Stack>

        <LoadingOverlay
          onClose={onSubmissionClose}
          open={displaySubmissions}
          container={props.root}
          transition="zoom"
        >
          <AssignmentModalComponent
            lecture={props.lecture}
            assignment={props.assignment}
            latestSubmissions={latestSubmissions}
          />
        </LoadingOverlay>
      </CardContent>
      <CardActions>
        <Button size="small" onClick={e => setDisplaySubmissions(true)}>
          View Assignment
        </Button>
      </CardActions>
    </Card>
  );
};
