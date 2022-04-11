import * as React from 'react';
import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import {
  generateAssignment,
  pullAssignment,
  pushAssignment,
  updateAssignment
} from '../../../services/assignments.service';
import GetAppRoundedIcon from '@mui/icons-material/GetAppRounded';
import { AgreeDialog, CommitDialog } from '../dialog';
import {
  Button,
  Card,
  Grid,
  CardHeader,
  CardContent,
  CardActions,
  Tabs,
  Tab,
  Box,
  IconButton,
  Tooltip
} from '@mui/material';
import ReplayIcon from '@mui/icons-material/Replay';
import { FilesList } from '../../util/file-list';
import { Settings } from './settings-menu';
import { GlobalObjects } from '../../../index';
import { Contents } from '@jupyterlab/services';
import moment from 'moment';
import { useEffect } from 'react';

export interface IFilesProps {
  lecture: Lecture;
  assignment: Assignment;
  onAssignmentChange: (assignment: Assignment) => void;
  showAlert: (severity: string, msg: string) => void;
}

export const Files = (props: IFilesProps) => {
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
  const [reloadFilesToggle, reloadFiles] = React.useState(false);

  const [srcChangedTimestamp, setSrcChangeTimestamp] = React.useState(
    moment().valueOf()
  ); // now
  const [generateTimestamp, setGenerateTimestamp] = React.useState(null);

  useEffect(() => {
    const srcPath = `source/${lecture.code}/${assignment.name}`;
    GlobalObjects.docManager.services.contents.fileChanged.connect(
      (sender: Contents.IManager, change: Contents.IChangedArgs) => {
        const { oldValue, newValue } = change;
        if (!newValue.path.includes(srcPath)) {
          return;
        }

        const modified = moment(newValue.last_modified).valueOf();
        if (srcChangedTimestamp === null || srcChangedTimestamp < modified) {
          setSrcChangeTimestamp(modified);
          console.log('New source file changed timestamp: ' + modified);
        }
      },
      this
    );
  }, [props]);

  const handleSwitchDir = async (dir: 'source' | 'release') => {
    if (dir === 'release') {
      if (
        generateTimestamp === null ||
        generateTimestamp < srcChangedTimestamp
      ) {
        try {
          await generateAssignment(lecture.id, assignment);
        } catch (err) {
          props.showAlert('error', 'Error Generating Assignment');
          return;
        }
        setGenerateTimestamp(moment().valueOf());
      }
    }
    setSelectedDir(dir);
  };

  const closeDialog = () => setShowDialog(false);

  const handlePushAssignment = async (commitMessage: string) => {
    setDialogContent({
      title: 'Push Assignment',
      message: `Do you want to push ${assignment.name}? This updates the state of the assignment on the server with your local state.`,
      handleAgree: async () => {
        try {
          // Note: has to be in this order (release -> source)
          await pushAssignment(lecture.id, assignment.id, 'release');
          await pushAssignment(
            lecture.id,
            assignment.id,
            'source',
            commitMessage
          );
        } catch (err) {
          props.showAlert('error', 'Error Pushing Assignment');
          closeDialog();
          return;
        }
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
        reloadFiles(!reloadFilesToggle);
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  return (
    <Card elevation={3}>
      <CardHeader
        title="Files"
        action={
          <Grid container>
            <Grid item>
              <Tooltip title="Reload">
                <IconButton
                  aria-label="reload"
                  onClick={() => reloadFiles(!reloadFilesToggle)}
                >
                  <ReplayIcon />
                </IconButton>
              </Tooltip>
            </Grid>
            <Grid item>
              <Settings
                lecture={lecture}
                assignment={assignment}
                selectedDir={selectedDir}
              />
            </Grid>
          </Grid>
        }
      />

      <CardContent sx={{ height: '270px', overflowY: 'auto' }}>
        <Tabs
          variant="fullWidth"
          value={selectedDir}
          onChange={(e, dir) => handleSwitchDir(dir)}
        >
          <Tab label="Source" value="source" />
          <Tab label="Release" value="release" />
        </Tabs>
        <Box height={214} sx={{ overflowY: 'auto' }}>
          <FilesList
            path={`${selectedDir}/${props.lecture.code}/${props.assignment.name}`}
            reloadFiles={reloadFilesToggle}
            showAlert={props.showAlert}
          />
        </Box>
      </CardContent>
      <CardActions>
        <CommitDialog handleSubmit={msg => handlePushAssignment(msg)} />
        <Button
          sx={{ mt: -1, ml: 2 }}
          onClick={() => handlePullAssignment()}
          variant="outlined"
          size="small"
        >
          <GetAppRoundedIcon fontSize="small" sx={{ mr: 1 }} />
          Pull
        </Button>
      </CardActions>
      <AgreeDialog open={showDialog} {...dialogContent} />
    </Card>
  );
};
