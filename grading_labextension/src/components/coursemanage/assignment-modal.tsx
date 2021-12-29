import * as React from 'react';
import {
    Badge,
    BottomNavigation,
    BottomNavigationAction,
    Box,
    Paper,
} from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { getAllSubmissions } from '../../services/submissions.service';
import { GradingComponent } from './grading';
import { AssignmentFileView } from './file-view';


export interface IAssignmentModalProps {
    lecture: Lecture;
    assignment: Assignment;
}

export const AssignmentModalComponent = (props: IAssignmentModalProps) => {

    const [latestSubmissions, setSubmissions] = React.useState(null);
    const [navigation, setNavigation] = React.useState(0);

    React.useEffect(() => {
        getAllSubmissions(props.lecture, props.assignment, true, true).then(
            (response: any) => {
                setSubmissions(response);
            }
        );
    }, [navigation]);

    return (
        <Box>
            <Box>
            {navigation == 0 && <AssignmentFileView lecture={props.lecture}
              assignment={props.assignment}
              latest_submissions={latestSubmissions}/>}

            {navigation == 1 && <GradingComponent lecture={props.lecture}
              assignment={props.assignment}
              latest_submissions={latestSubmissions}/>}
            </Box>

            <Paper sx={{ position: "absolute", bottom: 0, left: 0, right: 0 }} elevation={3}>
                <BottomNavigation
                    showLabels
                    value={navigation}
                    onChange={(event, newValue) => {
                        console.log(newValue);
                        setNavigation(newValue);
                    }}
                >
                    <BottomNavigationAction label="Overview" icon={<MoreVertIcon />} />
                    <BottomNavigationAction label="Submissions" icon={<Badge color="secondary"
                badgeContent={latestSubmissions?.length}
                showZero={latestSubmissions !== null}><MoreVertIcon /></Badge>} />
                </BottomNavigation>
            </Paper>
        </Box>
    );
}