import * as React from 'react';
import {
    AlertProps,
    Badge,
    Box,
    Button,
    Card,
    Grid,
    Snackbar,
    SpeedDial,
    SpeedDialAction,
    ToggleButton,
    ToggleButtonGroup,
    Typography,
    Portal,
    CardHeader,
    CardContent,
    CardActions
} from '@mui/material';
import IconButton, { IconButtonProps } from '@mui/material/IconButton';

import MuiAlert from '@mui/material/Alert';

import FormatListBulletedRoundedIcon from '@mui/icons-material/FormatListBulletedRounded';
import TerminalRoundedIcon from '@mui/icons-material/TerminalRounded';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import PublishRoundedIcon from '@mui/icons-material/PublishRounded';
import GetAppRoundedIcon from '@mui/icons-material/GetAppRounded';
import NewReleasesRoundedIcon from '@mui/icons-material/NewReleasesRounded';
import CloudDoneRoundedIcon from '@mui/icons-material/CloudDoneRounded';
import { FilesList } from '../util/file-list';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { GlobalObjects } from '../../index';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { ITerminal } from '@jupyterlab/terminal';
import { Terminal } from '@jupyterlab/services';
import { PageConfig } from '@jupyterlab/coreutils';
import { getAllSubmissions } from '../../services/submissions.service';
import { GradingComponent } from './grading';
import { AgreeDialog, EditDialog, IAgreeDialogProps } from './dialog';
import {
    pullAssignment,
    pushAssignment,
    updateAssignment
} from '../../services/assignments.service';
import { ModalTitle } from '../util/modal-title';

export interface IAssignmentFileViewProps {
    assignment: Assignment;
    lecture: Lecture;
    latest_submissions: any;
}

export const AssignmentFileView = (props: IAssignmentFileViewProps) => {
    const [assignment, setAssignment] = React.useState(props.assignment);
    const [alert, setAlert] = React.useState(false);
    const [severity, setSeverity] = React.useState('success');
    const [alertMessage, setAlertMessage] = React.useState('');
    const [selectedDir, setSelectedDir] = React.useState('source');
    const [latestSubmissions, setSubmissions] = React.useState(null);
    const [showDialog, setShowDialog] = React.useState(false);
    const [dialogContent, setDialogContent] = React.useState({
        title: '',
        message: '',
        handleAgree: null,
        handleDisagree: null
    });

    const serverRoot = PageConfig.getOption('serverRoot');

    const lecture = props.lecture;
    let terminalSession: Terminal.ITerminalConnection = null;

    const closeDialog = () => setShowDialog(false);

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

    const handlePushAssignment = async () => {
        setDialogContent({
            title: 'Push Assignment',
            message: `Do you want to push ${assignment.name}? This updates the state of the assignment on the server with your local state.`,
            handleAgree: async () => {
                try {
                    await pushAssignment(lecture.id, assignment.id, 'source');
                    await pushAssignment(lecture.id, assignment.id, 'release');
                } catch (err) {
                    showAlert('error', 'Error Pushing Assignment');
                }
                //TODO: should be atomar with the pushAssignment function
                const a = assignment;
                a.status = 'pushed';
                updateAssignment(lecture.id, a).then(
                    assignment => {
                        setAssignment(assignment);
                        showAlert('success', 'Successfully Pushed Assignment');
                    },
                    error => showAlert('error', 'Error Updating Assignment')
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
                    showAlert('success', 'Successfully Pulled Assignment');
                } catch (err) {
                    showAlert('error', 'Error Pulling Assignment');
                }
                // TODO: update file list
                closeDialog();
            },
            handleDisagree: () => closeDialog()
        });
        setShowDialog(true);
    };

    const handleReleaseAssignment = async () => {
        setDialogContent({
            title: 'Release Assignment',
            message: `Do you want to release ${assignment.name} for all students?`,
            handleAgree: () => {
                setDialogContent({
                    title: 'Confirmation',
                    message: `Are you sure you want to release ${assignment.name}?`,
                    handleAgree: async () => {
                        try {
                            console.log('releasing assignment');
                            let a = assignment;
                            a.status = 'released';
                            a = await updateAssignment(lecture.id, a);
                            setAssignment(a);
                            showAlert('success', 'Successfully Released Assignment');
                        } catch (err) {
                            showAlert('error', 'Error Releasing Assignment');
                        }
                        closeDialog();
                    },
                    handleDisagree: () => closeDialog()
                });
            },
            handleDisagree: () => closeDialog()
        });
        setShowDialog(true);
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
        <Box>
            <ModalTitle title={assignment.name} />
            <Box sx={{ ml: 3, mr: 3 }}>
                <Grid container spacing={3} alignItems="stretch">

                    <Grid item xs={6}>
                        <Card elevation={3}>

                            <CardHeader title="Files"
                                action={
                                    <SpeedDial
                                        direction="left"
                                        ariaLabel="SpeedDial openIcon example"
                                        icon={<MoreVertIcon />}
                                        FabProps={{ size: 'medium' }}
                                    >
                                        {actions.map(action => (
                                            <SpeedDialAction
                                                onClick={action.onClick}
                                                key={action.name}
                                                icon={action.icon}
                                                tooltipTitle={action.name}
                                            />
                                        ))}
                                    </SpeedDial>} />


                            <CardContent>
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
                                <Button
                                    sx={{ mt: -1 }}
                                    onClick={() => handlePushAssignment()}
                                    variant="outlined"
                                    size="small"
                                >
                                    <PublishRoundedIcon fontSize="small" sx={{ mr: 1 }} />
                                    Push
                                </Button>
                                <Button
                                    sx={{ mt: -1 }}
                                    onClick={() => handlePullAssignment()}
                                    variant="outlined"
                                    size="small"
                                >
                                    <GetAppRoundedIcon fontSize="small" sx={{ mr: 1 }} />
                                    Pull
                                </Button>
                                <Button
                                    sx={{ mt: -1 }}
                                    onClick={() => handleReleaseAssignment()}
                                    variant="outlined"
                                    size="small"
                                >
                                    <NewReleasesRoundedIcon fontSize="small" sx={{ mr: 1 }} />
                                    Release
                                </Button>
                            </CardActions>
                        </Card>
                    </Grid>
                    <Grid item xs={6}>
                        <Card elevation={3}>
                            <CardHeader title="Stats or other stuff" />
                            <CardContent>
                                <Box sx={{ height: 300, backgroundColor: 'primary.dark' }}>

                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                    <AgreeDialog open={showDialog} {...dialogContent} />
                    <Portal container={document.body}>
                        <Snackbar
                            open={alert}
                            autoHideDuration={3000}
                            onClose={handleAlertClose}
                            sx={{ mb: 2, ml: 2 }}
                        >
                            <MuiAlert
                                onClose={handleAlertClose}
                                severity={severity as AlertProps['severity']}
                                sx={{ width: '100%' }}
                            >
                                {alertMessage}
                            </MuiAlert>
                        </Snackbar>
                    </Portal>
                </Grid>
            </Box>
        </Box>

    );
};
