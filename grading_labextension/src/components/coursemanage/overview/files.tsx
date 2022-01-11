import * as React from 'react';
import {Assignment} from '../../../model/assignment';
import {Lecture} from '../../../model/lecture';
import {getAssignment, pullAssignment, pushAssignment, updateAssignment} from '../../../services/assignments.service';
import PublishRoundedIcon from '@mui/icons-material/PublishRounded';
import GetAppRoundedIcon from '@mui/icons-material/GetAppRounded';
import NewReleasesRoundedIcon from '@mui/icons-material/NewReleasesRounded';
import MuiAlert from '@mui/material/Alert';
import {AgreeDialog} from '../dialog';
import {
  AlertProps,
  Button,
  Card,
  ToggleButton,
  ToggleButtonGroup,
  CardHeader,
  CardContent,
  CardActions,
  Snackbar,
  Tabs,
  Tab,
  Box
} from '@mui/material';
import {FilesList} from '../../util/file-list';
import {Settings} from './settings-menu';

export interface FilesProps {
  lecture: Lecture;
  assignment: Assignment;
  onAssignmentChange: (assignment: Assignment) => void;
  showAlert: (severity: string, msg: string) => void;
}

export const Files = (props: FilesProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const [lecture, setLecture] = React.useState(props.lecture);
  const [selectedDir, setSelectedDir] = React.useState('source');
  const [showDialog, setShowDialog] = React.useState(false);
  const [dialogContent, setDialogContent] = React.useState({
    title: '',
    message: '',
    handleAgree: null,
    handleDisagree: null
  });

  const closeDialog = () => setShowDialog(false);

  const handlePushAssignment = async () => {
    setDialogContent({
      title: 'Push Assignment',
      message: `Do you want to push ${assignment.name}? This updates the state of the assignment on the server with your local state.`,
      handleAgree: async () => {
        try {
          await pushAssignment(lecture.id, assignment.id, 'source');
          await pushAssignment(lecture.id, assignment.id, 'release');
        } catch (err) {
          props.showAlert('error', 'Error Pushing Assignment');
        }
        //TODO: should be atomar with the pushAssignment function
        const a = assignment;
        a.status = 'pushed';
        updateAssignment(lecture.id, a).then(
          assignment => {
            setAssignment(assignment);
            props.showAlert('success', 'Successfully Pushed Assignment');
            props.onAssignmentChange(assignment);
          },
          error => props.showAlert('error', 'Error Updating Assignment')
        );
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  const handlePullAssignment = async () => {
    setDialogContent({
      title: 'Pull Assignment',
      message: `Do you want to pull ${assignment.name}? This updates your assignment with the state of the server and overwrites all changes.`,
      handleAgree: async () => {
        try {
          await pullAssignment(lecture.id, assignment.id, 'source');
          props.showAlert('success', 'Successfully Pulled Assignment');
        } catch (err) {
          props.showAlert('error', 'Error Pulling Assignment');
        }
        // TODO: update file list
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  return (
    <Card className='flexbox-item' elevation={3}>

      <CardHeader title="Files"
                  action={
                    <Settings lecture={lecture} assignment={assignment} selectedDir={selectedDir}/>
                  }/>

      <CardContent sx={{height: '270px', width: '300px', overflowY: "auto"}}>
        <Tabs variant='fullWidth' value={selectedDir} onChange={(e, dir) => setSelectedDir(dir)}>
          <Tab label="Source" value="source"/>
          <Tab label="Release" value="release"/>
        </Tabs>
        <Box height={214} overflow={'scroll'}>
          <FilesList
            path={`${selectedDir}/${props.lecture.code}/${props.assignment.name}`}
          />
        </Box>
      </CardContent>
      <CardActions>
        <Button
          sx={{mt: -1}}
          onClick={() => handlePushAssignment()}
          variant="outlined"
          size="small"
        >
          <PublishRoundedIcon fontSize="small" sx={{mr: 1}}/>
          Push
        </Button>
        <Button
          sx={{mt: -1}}
          onClick={() => handlePullAssignment()}
          variant="outlined"
          size="small"
        >
          <GetAppRoundedIcon fontSize="small" sx={{mr: 1}}/>
          Pull
        </Button>
      </CardActions>
      <AgreeDialog open={showDialog} {...dialogContent} />
    </Card>

  );
}