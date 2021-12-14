import * as React from 'react';
import {
  Badge,
  Box,
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  Collapse,
  IconButton,
  Snackbar,
  SpeedDial,
  SpeedDialAction,
  ToggleButton,
  ToggleButtonGroup,
  Typography
} from '@mui/material';
import MuiAlert, { AlertProps } from '@mui/material/Alert';

import FormatListBulletedRoundedIcon from '@mui/icons-material/FormatListBulletedRounded';
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded';
import LayersRoundedIcon from '@mui/icons-material/LayersRounded';
import EditIcon from '@mui/icons-material/Edit';
import PublishRoundedIcon from '@mui/icons-material/PublishRounded';
import GetAppRoundedIcon from '@mui/icons-material/GetAppRounded';
import NewReleasesRoundedIcon from '@mui/icons-material/NewReleasesRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';
import { FilesList } from '../util/file-list';
import { Assignment } from '../../model/assignment';
import LoadingOverlay from '../util/overlay';
import { Lecture } from '../../model/lecture';
import { GlobalObjects } from '../../index';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { ITerminal } from '@jupyterlab/terminal';
import { Terminal } from '@jupyterlab/services';
import { PageConfig } from '@jupyterlab/coreutils';

interface IAssignmentComponentProps {
  lecture: Lecture;
  assignment: Assignment;
  root: HTMLElement;
}

export const AssignmentComponent = (props: IAssignmentComponentProps) => {
  const [expanded, setExpanded] = React.useState(false);
  const [alert, setAlert] = React.useState(false);
  const [severity, setSeverity] = React.useState('success');
  const [alertMessage, setAlertMessage] = React.useState('');
  const [selectedDir, setSelectedDir] = React.useState('source');
  const [displaySubmissions, setDisplaySubmissions] = React.useState(false);
  const onSubmissionClose = () => setDisplaySubmissions(false);

  const serverRoot = PageConfig.getOption('serverRoot');

  const assignment = props.assignment;
  const lecture = props.lecture;
  let terminalSession: Terminal.ITerminalConnection = null;

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const openTerminal = async () => {
    const path = `${serverRoot}/${selectedDir}/${lecture.code}/${assignment.name}`;
    console.log('Opening terminal at: ' + path.replace(' ', '\\ '));
    let args = {};
    if (
      terminalSession !== null &&
      terminalSession.connectionStatus === 'connected'
    ) {
      args = { name: terminalSession.name };
    }
    const main = (await GlobalObjects.commands.execute(
      'terminal:open',
      args
    )) as MainAreaWidget<ITerminal.ITerminal>;

    if (main) {
      const terminal = main.content;
      terminalSession = terminal.session;
    }

    try {
      terminalSession.send({
        type: 'stdin',
        content: ['cd ' + path.replace(' ', '\\ ') + '\n']
      });
    } catch (e) {
      showAlert('error', 'Error Opening Terminal');
      main.dispose();
    }
  };

  const openBrowser = async () => {
    const path = `${selectedDir}/${lecture.code}/${assignment.name}`;
    GlobalObjects.commands
      .execute('filebrowser:go-to-path', {
        path
      })
      .catch(error => {
        showAlert('error', 'Error showing in File Browser');
      });
  };

  const showAlert = (severity: string, msg: string) => {
    setSeverity(severity);
    setAlertMessage(msg);
    setAlert(true);
  };

  const handleAlertClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === 'clickaway') {
      return;
    }
    setAlert(false);
  };

  const actions = [
    {
      icon: <FormatListBulletedRoundedIcon />,
      name: 'Show Files',
      onClick: () => openBrowser()
    },
    {
      icon: <TerminalRoundedIcon />,
      name: 'Open Terminal',
      onClick: () => openTerminal()
    }
  ];

  return (
    <Box sx={{ minWidth: 275 }}>
      <Card variant="outlined">
        <CardActionArea onClick={handleExpandClick}>
          <CardContent>
            <Typography
              sx={{ mb: 1, display: 'inline' }}
              variant="h5"
              component="div"
            >
              {assignment.name}
            </Typography>
            <IconButton
              sx={{ mt: -1 }}
              onClick={e => {
                e.stopPropagation();
              }}
              aria-label="edit"
            >
              <EditIcon />
            </IconButton>
          </CardContent>
        </CardActionArea>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Typography variant="h6">Files</Typography>
            <ToggleButtonGroup
              color="secondary"
              value={selectedDir}
              exclusive
              onChange={(e, dir) => setSelectedDir(dir)}
              size="small"
            >
              <ToggleButton color="primary" value="source">
                Source
              </ToggleButton>
              <ToggleButton value="release">Release</ToggleButton>
            </ToggleButtonGroup>
            <FilesList
              path={`${selectedDir}/${props.lecture.code}/${props.assignment.name}`}
            />
          </CardContent>
          <CardActions>
            <SpeedDial
              direction="right"
              ariaLabel="SpeedDial openIcon example"
              icon={<LayersRoundedIcon />}
              FabProps={{ size: 'medium' }}
              sx={{ mt: -2, mr: 'auto' }}
            >
              {actions.map(action => (
                <SpeedDialAction
                  onClick={action.onClick}
                  key={action.name}
                  icon={action.icon}
                  tooltipTitle={action.name}
                />
              ))}
            </SpeedDial>

            <Button
              sx={{ mt: -1 }}
              onClick={() => showAlert('success', 'Push')}
              variant="outlined"
              size="small"
            >
              <PublishRoundedIcon fontSize="small" sx={{ mr: 1 }} />
              Push
            </Button>
            <Button
              sx={{ mt: -1 }}
              onClick={() => showAlert('error', 'Pull')}
              variant="outlined"
              size="small"
            >
              <GetAppRoundedIcon fontSize="small" sx={{ mr: 1 }} />
              Pull
            </Button>
            <Button
              sx={{ mt: -1 }}
              onClick={() => showAlert('error', 'Release')}
              variant="outlined"
              size="small"
            >
              <NewReleasesRoundedIcon fontSize="small" sx={{ mr: 1 }} />
              Release
            </Button>
            <Badge
              sx={{ mt: -1, mr: 2, ml: 1 }}
              color="secondary"
              badgeContent={0}
              showZero
            >
              <Button
                sx={{ ml: 'auto' }}
                onClick={() => setDisplaySubmissions(true)}
                variant="outlined"
                size="small"
              >
                <CloudDoneRoundedIcon fontSize="small" sx={{ mr: 1 }} />
                Submissions
              </Button>
            </Badge>
            <LoadingOverlay
              onClose={onSubmissionClose}
              open={displaySubmissions}
              container={props.root}
            >
              <Typography variant={'h2'}>Submissions</Typography>
            </LoadingOverlay>
          </CardActions>
        </Collapse>
      </Card>

      <Snackbar open={alert} autoHideDuration={3000} onClose={handleAlertClose}>
        <MuiAlert
          onClose={handleAlertClose}
          severity={severity as AlertProps['severity']}
          sx={{ width: '100%' }}
        >
          {alertMessage}
        </MuiAlert>
      </Snackbar>
    </Box>
  );
};
