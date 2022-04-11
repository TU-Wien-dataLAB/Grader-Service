import * as React from 'react';

import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import { EditDialog } from '../dialog';
import { ModalTitle } from '../../util/modal-title';
import { GradingChart, SubmittedChart } from './charts';
import { OverviewCard } from './overview-card';
import { Box, Grid } from '@mui/material';
import { Files } from './files';
import { GitLog } from './git-log';
import { getAssignment } from '../../../services/assignments.service';
import { AssignmentStatus } from './assignment-status';
import { RepoType } from '../../util/repo-type';

export interface IOverviewProps {
  assignment: Assignment;
  lecture: Lecture;
  allSubmissions: any[];
  latest_submissions: any;
  users: any;
  showAlert: (severity: string, msg: string) => void;
}

export const OverviewComponent = (props: IOverviewProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const lecture = props.lecture;

  const onAssignmentChange = (assignment: Assignment) => {
    setAssignment(assignment);
  };

  return (
    <Box>
      <ModalTitle title={assignment.name}>
        <Box sx={{ ml: 2 }} display="inline-block">
          <EditDialog
            lecture={props.lecture}
            assignment={assignment}
            onSubmit={() =>
              getAssignment(lecture.id, assignment).then(assignment =>
                setAssignment(assignment)
              )
            }
          />
        </Box>
      </ModalTitle>
      <Box sx={{ ml: 3, mr: 3, mb: 3, mt: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={12} lg={12}>
            <AssignmentStatus
              lecture={props.lecture}
              assignment={assignment}
              onAssignmentChange={onAssignmentChange}
              showAlert={props.showAlert}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <OverviewCard
              assignment={assignment}
              allSubmissions={props.allSubmissions}
              users={props.users}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <Files
              lecture={lecture}
              assignment={assignment}
              onAssignmentChange={onAssignmentChange}
              showAlert={props.showAlert}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <GitLog
              lecture={lecture}
              assignment={assignment}
              repoType={RepoType.SOURCE}
            />
          </Grid>

          <Grid item xs={12} md={3} lg={3}>
            <SubmittedChart
              lecture={lecture}
              assignment={assignment}
              allSubmissions={props.allSubmissions}
              users={props.users}
            />
          </Grid>

          <Grid item xs={12} md={3} lg={3}>
            <GradingChart
              lecture={lecture}
              assignment={assignment}
              allSubmissions={props.allSubmissions}
              users={props.users}
            />
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};
