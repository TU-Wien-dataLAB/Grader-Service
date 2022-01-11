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

export interface IAssignmentFileViewProps {
  assignment: Assignment;
  lecture: Lecture;
  allSubmissions: any[];
  latest_submissions: any;
  showAlert: (severity: string, msg: string) => void;
}

export const AssignmentFileView = (props: IAssignmentFileViewProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const lecture = props.lecture;


  return (
    <Box>
      <ModalTitle title={assignment.name}>
        <Box sx={{ml: 2}} display="inline-block">
          <EditDialog lecture={props.lecture} assignment={assignment}/>
        </Box>
      </ModalTitle>
      <Box className='flexbox-panel' sx={{ml: 3, mr: 3, mb: 3, mt: 9}}>

        <OverviewCard assignment={assignment} allSubmissions={props.allSubmissions}/>

        <Files lecture={lecture} assignment={assignment}
               onGitAction={async () => setAssignment(await getAssignment(props.lecture.id, assignment))}
               showAlert={props.showAlert}
        />

        <GitLog lecture={lecture} assignment={assignment}/>

        <SubmittedChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions}/>

        <GradingChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions}/>

      </Box>
    </Box>

  );
};
