import * as React from 'react';

import IconButton, { IconButtonProps } from '@mui/material/IconButton';

import MuiAlert from '@mui/material/Alert';

import FormatListBulletedRoundedIcon from '@mui/icons-material/FormatListBulletedRounded';
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import PublishRoundedIcon from '@mui/icons-material/PublishRounded';
import GetAppRoundedIcon from '@mui/icons-material/GetAppRounded';
import NewReleasesRoundedIcon from '@mui/icons-material/NewReleasesRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';
import { FilesList } from '../../util/file-list';
import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import { GlobalObjects } from '../../../index';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { ITerminal } from '@jupyterlab/terminal';
import { Terminal } from '@jupyterlab/services';
import { PageConfig } from '@jupyterlab/coreutils';
import { getAllSubmissions } from '../../../services/submissions.service';
import { GradingComponent } from '../grading';
import { EditDialog } from '../dialog';
import {
    pullAssignment,
    pushAssignment,
    updateAssignment
} from '../../../services/assignments.service';
import { ModalTitle } from '../../util/modal-title';
import { GradingChart, SubmittedChart } from './charts';
//import { OverviewCard } from './overview-card';
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

                {/*<OverviewCard />*/}

                <Files lecture={lecture} assignment={assignment} />

                <SubmittedChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions} />

                <GradingChart lecture={lecture} assignment={assignment} allSubmissions={props.allSubmissions} />

                
            </Box>
        </Box>

    );
};
