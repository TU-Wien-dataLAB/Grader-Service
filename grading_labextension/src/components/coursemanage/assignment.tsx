import * as React from 'react';
import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  Typography
} from '@mui/material';

import { Assignment } from '../../model/assignment';
import LoadingOverlay from '../util/overlay';
import { Lecture } from '../../model/lecture';
import { getAllSubmissions } from '../../services/submissions.service';
import { AssignmentModalComponent } from './assignment-modal';

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [displaySubmissions, setDisplaySubmissions] = React.useState(false);

  const onSubmissionClose = () => setDisplaySubmissions(false);

  return (
    <Box sx={{ minWidth: 275 }}>
      <Card variant="outlined">
        <CardActionArea onClick={(e) => setDisplaySubmissions(true)
        }>
          <CardContent>
            <Typography
              sx={{ mb: 1, display: 'inline' }}
              variant="h5"
              component="div"
            >
              {props.assignment.name}
            </Typography>

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
          assignment={props.assignment} 
          />
      </LoadingOverlay>
    </Box>
  );
};
