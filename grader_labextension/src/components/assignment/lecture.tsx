// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Collapse,
  LinearProgress,
  Typography
} from '@mui/material';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { getAllAssignments } from '../../services/assignments.service';
import { AssignmentComponent } from './assignment';

interface ILectureComponentProps {
  lecture: Lecture;
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
  open?: boolean;
}

export const LectureComponent = (props: ILectureComponentProps) => {
  const [assignments, setAssignments] = React.useState(null as Assignment[]);
  const [expanded, setExpanded] = React.useState(props.open);

  React.useEffect(() => {
    getAllAssignments(props.lecture.id).then(response => {
      setAssignments(response);
    });
  }, []);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  if (assignments === null) {
    return (
      <div>
        <Card>
          <LinearProgress />
        </Card>
      </div>
    );
  }
  if (assignments.length === 0) {
    return null;
  }
  return (
    <div>
      <Card
        sx={{ backgroundColor: expanded ? '#fafafa' : 'background.paper' }}
        elevation={expanded ? 0 : 2}
        className="lecture-card"
      >
        <CardContent sx={{ mb: -1, display: 'flex' }}>
          <Typography variant={'h5'} sx={{ mr: 2 }}>
            {props.lecture.name}
          </Typography>
        </CardContent>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
              {assignments.map((el: Assignment) => (
                <AssignmentComponent
                  lecture={props.lecture}
                  assignment={el}
                  root={props.root}
                  showAlert={props.showAlert}
                />
              ))}
            </Box>
          </CardContent>
        </Collapse>
        <CardActions>
          <Button size="small" sx={{ ml: 'auto' }} onClick={handleExpandClick}>
            {(expanded ? 'Hide' : 'Show') + ' Assignments'}
          </Button>
        </CardActions>
      </Card>
    </div>
  );
};
