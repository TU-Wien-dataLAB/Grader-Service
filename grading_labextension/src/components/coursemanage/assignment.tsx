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
import { getAssignment } from '../../services/assignments.service';
import { AssignmentModalComponent } from './assignment-modal';
import { DeadlineComponent } from '../util/deadline';

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const [displaySubmissions, setDisplaySubmissions] = React.useState(false);
  const onSubmissionClose = async () => {
    setDisplaySubmissions(false);
    setAssignment(await getAssignment(props.lecture.id, assignment));
  };

  const [latestSubmissions, setSubmissions] = React.useState([]);
  React.useEffect(() => {
    getAllSubmissions(props.lecture, assignment, true, true).then(
      (response: any) => {
        setSubmissions(response);
      }
    );
  }, [props]);

  return (
    <Box>
      <Card
        sx={{ maxWidth: 225, minWidth: 225, m: 1.5 }}
        onClick={e => setDisplaySubmissions(true)}
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
                component={"chip"}
              />
              <Chip
                sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                size="small"
                icon={<AssignmentTurnedInRoundedIcon />}
                label={assignment.status}
              />
              <Chip
                sx={{ margin: 'auto', ml: 0, mt: 0.75 }}
                size="small"
                icon={<CloudDoneRoundedIcon />}
                label={'Submissions: ' + latestSubmissions.length}
              />
            </Stack>
          </CardContent>
        </CardActionArea>
      </Card>
      <LoadingOverlay
        onClose={onSubmissionClose}
        open={displaySubmissions}
        container={props.root}
        transition="zoom"
      >
        <AssignmentModalComponent
          lecture={props.lecture}
          assignment={assignment}
          latestSubmissions={latestSubmissions}
        />
      </LoadingOverlay>
    </Box>
  );
};
