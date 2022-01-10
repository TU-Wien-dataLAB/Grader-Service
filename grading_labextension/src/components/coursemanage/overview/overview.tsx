import * as React from 'react';

import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import { EditDialog } from '../dialog';
import { ModalTitle } from '../../util/modal-title';
import { GradingChart, SubmittedChart } from './charts';
import { OverviewCard } from './overview-card';
import { Box } from '@mui/material';
import { Files } from './files';

export interface IAssignmentFileViewProps {
    assignment: Assignment;
    lecture: Lecture;
    allSubmissions: any[];
    latest_submissions: any;
}

export const AssignmentFileView = (props: IAssignmentFileViewProps) => {
    const [assignment, setAssignment] = React.useState(props.assignment);
    const lecture = props.lecture;


    return (
        <Box>
            <ModalTitle title={assignment.name} />
            <EditDialog lecture={props.lecture} assignment={assignment} />
            <Box className='flexbox-panel' sx={{ ml: 3, mr: 3, mb: 3, mt: 6 }}>

                <OverviewCard assignment={assignment} allSubmissions={props.allSubmissions}/>

                <Files lecture={lecture} assignment={assignment} />

                <SubmittedChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions} />

                <GradingChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions} />

                
            </Box>
        </Box>

    );
};
