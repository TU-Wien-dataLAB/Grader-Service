import * as React from 'react';
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  Chip, Divider,
  Stack,
  Typography
} from '@mui/material';

import AssignmentTurnedInRoundedIcon from '@mui/icons-material/AssignmentTurnedInRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';

import {Assignment} from '../../model/assignment';
import LoadingOverlay from '../util/overlay';
import {Lecture} from '../../model/lecture';
import {getAllSubmissions} from '../../services/submissions.service';
import {getAssignment} from '../../services/assignments.service';
import {AssignmentModalComponent} from './assignment-modal';
import {DeadlineComponent} from '../util/deadline';
import {blue} from "@mui/material/colors";
import {getFiles} from "../../services/file.service";
import CheckCircleOutlineOutlinedIcon from "@mui/icons-material/CheckCircleOutlineOutlined";
import CancelOutlinedIcon from "@mui/icons-material/CancelOutlined";

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
  users: any;
  showAlert: (severity: string, msg: string) => void;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const [displaySubmissions, setDisplaySubmissions] = React.useState(false);
  const [files, setFiles] = React.useState([]);
  const onSubmissionClose = async () => {
    setDisplaySubmissions(false);
    setAssignment(await getAssignment(props.lecture.id, assignment));
  };

  const [allSubmissions, setAllSubmissions] = React.useState([]);
  const [latestSubmissions, setLatestSubmissions] = React.useState([]);
  const [numAutoGraded, setNumAutoGraded] = React.useState(0);
  const [numManualGraded, setNumManualGraded] = React.useState(0);
  React.useEffect(() => {

    getAllSubmissions(props.lecture, assignment, false, true).then(
      response => {
        setAllSubmissions(response);
        let auto = 0;
        let manual = 0;
          for (const submission of response) {
            if (submission.auto_status === "automatically_graded") auto++;
            if (submission.manual_status === "manually_graded") manual++;
          }
        setNumAutoGraded(auto);
        setNumManualGraded(manual);
      })

      getAllSubmissions(props.lecture, assignment, true, true).then(
        response => {
          setLatestSubmissions(response);
        })

      getFiles(`source/${props.lecture.code}/${assignment.name}`).then(files => {
        setFiles(files)
      })
    }, [props]
  );

  return (
    <Box>
      <Card
        sx={{maxWidth: 225, minWidth: 225, m: 1.5}}
        onClick={e => setDisplaySubmissions(true)}
      >
        <CardActionArea>
          <CardContent>
            <Typography variant="h5" component="div">
              {assignment.name}
            </Typography>
            <Typography sx={{fontSize: 14}} color="text.secondary" gutterBottom>
              {files.length + ' File' + (files.length === 1 ? '' : 's')}
              <Typography sx={{fontSize: 12, display: "inline-block", color: blue[500], float: "right"}}>
                {assignment.status}
              </Typography>
            </Typography>
            <Divider sx={{mt: 1, mb: 1}}/>

            <Typography sx={{fontSize: 15, mt: 0.5, ml: 0.5}}>
              {allSubmissions.length}
              <Typography
                color="text.secondary"
                sx={{
                  display: "inline-block",
                  ml: 0.75,
                  fontSize: 13
                }}
              >
                {'Submission' + (allSubmissions.length === 1 ? '' : 's')}
              </Typography>
            </Typography>
            <Typography sx={{fontSize: 15, mt: 0.5, ml: 0.5}}>
              {numAutoGraded}
              <Typography sx={{fontSize: 10, ml: 0, display: "inline-block"}}>
                {'/' + allSubmissions.length}
              </Typography>
              <Typography
                color="text.secondary"
                sx={{
                  display: "inline-block",
                  ml: 0.75,
                  fontSize: 13
                }}
              >
                {'Autograded Submission' + (numAutoGraded === 1 ? '' : 's')}
              </Typography>
            </Typography>
            <Typography sx={{fontSize: 15, mt: 0.5, ml: 0.5}}>
              {numManualGraded}
              <Typography sx={{fontSize: 10, ml: 0, display: "inline-block"}}>
                {'/' + allSubmissions.length}
              </Typography>
              <Typography
                color="text.secondary"
                sx={{
                  display: "inline-block",
                  ml: 0.75,
                  fontSize: 13
                }}
              >
                {'Manualgraded Submission' + (numManualGraded === 1 ? '' : 's')}
              </Typography>
            </Typography>
          </CardContent>
          <DeadlineComponent due_date={assignment.due_date} compact={false} component={"card"}/>
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
          allSubmissions={allSubmissions}
          latestSubmissions={latestSubmissions}
          root={props.root}
          users={props.users}
          showAlert={props.showAlert}
        />
      </LoadingOverlay>
    </Box>
  );
};
