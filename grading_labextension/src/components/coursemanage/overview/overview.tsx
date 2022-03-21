import * as React from 'react';

import {Assignment} from '../../../model/assignment';
import {Lecture} from '../../../model/lecture';
import {EditDialog} from '../dialog';
import {ModalTitle} from '../../util/modal-title';
import {GradingChart, SubmittedChart} from './charts';
import {OverviewCard} from './overview-card';
import {Box} from '@mui/material';
import {Files} from './files';
import {GitLog} from "./git-log";
import {getAssignment} from "../../../services/assignments.service";
import {AssignmentStatus} from "./assignment-status";

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
    setAssignment(assignment)
  }

  return (
    <Box>
      <ModalTitle title={assignment.name}>
        <Box sx={{ml: 2}} display="inline-block">
          <EditDialog lecture={props.lecture} assignment={assignment}
                      onSubmit={() => getAssignment(lecture.id, assignment).then(assignment => setAssignment(assignment))}/>
        </Box>
      </ModalTitle>
      <Box className='flexbox-panel' sx={{ml: 3, mr: 3, mb: 3, mt: 9}}>

        <OverviewCard assignment={assignment} allSubmissions={props.allSubmissions} users={props.users}/>

        <AssignmentStatus lecture={props.lecture} assignment={assignment}
                          onAssignmentChange={onAssignmentChange} showAlert={props.showAlert}/>

        <Files lecture={lecture} assignment={assignment}
               onAssignmentChange={onAssignmentChange}
               showAlert={props.showAlert}
        />

        <GitLog lecture={lecture} assignment={assignment}/>

        <SubmittedChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions}
                        users={props.users}/>

        <GradingChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions}
                      users={props.users}/>

      </Box>
    </Box>

  );
};
