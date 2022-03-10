import {DataGrid, GridRenderCellParams, GridRowId, GridSelectionModel} from '@mui/x-data-grid';
import * as React from 'react';
import {Assignment} from '../../model/assignment';
import {Lecture} from '../../model/lecture';
import {utcToLocalFormat} from '../../services/datetime.service';
import {
  Box,
  Button,
  Chip, Dialog,
  DialogActions,
  DialogContent, DialogContentText,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem, 
  Typography,
  Tooltip,
  IconButton
} from '@mui/material';
import Select, {SelectChangeEvent} from '@mui/material/Select';
import {getAllSubmissions} from '../../services/submissions.service';
import {AgreeDialog} from './dialog';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import {ModalTitle} from "../util/modal-title";
import {User} from "../../model/user";
import {Submission} from "../../model/submission";
import {autogradeSubmission, generateFeedback} from "../../services/grading.service";
import LoadingOverlay from "../util/overlay";
import {getAssignment} from "../../services/assignments.service";
import {ManualGrading} from "./manual-grading";
import {PanoramaSharp} from '@mui/icons-material';
import ReplayIcon from '@mui/icons-material/Replay';


export interface IGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  latest_submissions: Submission[];
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
}

interface IRowValues extends Submission {
  sub_id: number;
}

export const GradingComponent = (props: IGradingProps) => {
  const [option, setOption] = React.useState('latest');
  const [showDialog, setShowDialog] = React.useState(false);
  const [showLogs, setShowLogs] = React.useState(false);
  const [logs, setLogs] = React.useState(undefined);
  const [dialogContent, setDialogContent] = React.useState({
    title: '',
    message: '',
    handleAgree: null,
    handleDisagree: null
  });

  const [displayManualGrading, setDisplayManualGrading] = React.useState(false);
  const onManualGradingClose = async () => {
    setDisplayManualGrading(false);
  };

  const cleanSelectedRows = () => {
    setSelectedRows([]);
  }

  const handleAutogradeSubmissions = async () => {
    setDialogContent({
      title: 'Autograde Selected Submissions',
      message: `Do you wish to autograde the seleceted submissions?`,
      handleAgree: async () => {
        try {
          const numSubs = selectedRowsData.length
          await Promise.all(selectedRowsData.map(async (row) => {
            await autogradeSubmission(props.lecture, props.assignment, row)
            console.log("Autograded submission");
          }));
          const latest = option === 'latest' ? true : false;
          getAllSubmissions(props.lecture, props.assignment, latest, true).then(response => {
            setRows(generateRows(response));
            props.showAlert('success', `Grading ${numSubs} Submissions`);
          })
        } catch (err) {
          console.error(err);
          props.showAlert('error', 'Error Autograding Submissions');
        }
        cleanSelectedRows()
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  const handleGenerateFeedback = async () => {
    setDialogContent({
      title: 'Generate Feedback',
      message: `Do you wish to generate Feedback of the selected submissions?`,
      handleAgree: async () => {
        try {
          const numSubs = selectedRowsData.length
          await Promise.all(selectedRowsData.map(async (row) => {
            await generateFeedback(props.lecture.id, props.assignment.id, row.id)
            console.log("Autograded submission");
          }));
          getAllSubmissions(props.lecture, props.assignment, false, true).then(response => {
            setRows(generateRows(response));
            props.showAlert('success', `Generating Feedback for ${numSubs} Submissions`);
          })
        } catch (err) {
          console.error(err);
          props.showAlert('error', 'Error Generating Feedback');
        }
        cleanSelectedRows();
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  const closeDialog = () => setShowDialog(false);


  const generateRows = (submissions: Submission[]) => {
    console.log("Submissions");
    console.log(submissions);
    console.log("option: " + option);
    const rows: IRowValues[] = [];
    let id: number = 1;
    submissions.forEach((sub: Submission) => {
      rows.push({
        id: sub.id,
        sub_id: id++,
        username: sub.username,
        submitted_at: utcToLocalFormat(sub.submitted_at),
        auto_status: sub.auto_status,
        manual_status: sub.manual_status,
        logs: sub.logs,
        commit_hash: sub.commit_hash,
        feedback_available: sub.feedback_available,
        score: sub.score
      });
    });
    console.log(rows);
    return rows;
  };

  const [submissions, setSubmissions] = React.useState(props.latest_submissions);
  const [rows, setRows] = React.useState(generateRows(props.latest_submissions));
  const [selectedRows, setSelectedRows] = React.useState<GridSelectionModel>([]);
  const [selectedRowsData, setSelectedRowsData] = React.useState([] as IRowValues[]);


  const handleChange = (event: SelectChangeEvent) => {
    setOption(event.target.value as string);
  };

  const updateSubmissions = () => {
    const latest = option === 'latest' ? true : false;
    getAllSubmissions(props.lecture, props.assignment, latest, true).then(response => {
      setRows(generateRows(response));
      setSubmissions(response);
    })
  }

  React.useEffect(() => {
    updateSubmissions();
  }, [option]);


  const getColor = (value: string) => {
    if (value === 'not_graded') {
      return 'warning';
    } else if (value === 'automatically_graded' || value === 'manually_graded') {
      return 'success';
    } else if (value === 'grading_failed') {
      return 'error';
    }
    return 'primary'
  }

  const openLogs = (params: GridRenderCellParams<string>) => {
    const submission: Submission = getSubmissionFromRow(params.row as IRowValues);
    let logs = submission.logs;
    if (logs === undefined || logs === null || logs === "") {
      props.showAlert("error", "No logs for submission!");
      return;
    }
    setLogs(logs);
    setShowLogs(true);
  }

  const columns = [
    {field: 'sub_id', headerName: 'No.', width: 110},
    {field: 'username', headerName: 'User', width: 130},
    {field: 'submitted_at', headerName: 'Date', width: 170},
    {
      field: 'auto_status', headerName: 'Autograde-Status', width: 200,
      renderCell: (params: GridRenderCellParams<string>) => (

        <Chip variant='outlined' label={params.value} color={getColor(params.value)} clickable={true}
              onClick={() => openLogs(params)}/>
      ),
    },
    {
      field: 'manual_status', headerName: 'Manualgrade-Status', width: 170,
      renderCell: (params: GridRenderCellParams<string>) => (

        <Chip variant='outlined' label={params.value} color={getColor(params.value)}/>
      ),
    },
    {
      field: 'feedback_available', headerName: 'Feedback generated', width: 170,
      renderCell: (params: GridRenderCellParams<boolean>) => (
        <Chip variant='outlined' label={params.value ? 'Generated' : 'Not Generated'}
              color={params.value ? 'success' : 'error'}/>
      ),
    },
    {field: 'score', headerName: 'Score', width: 130}
  ];

  //TODO: Not perfomant 
  const getSubmissionFromRow = (row: IRowValues): Submission => {
    if (row === undefined) return null;
    const id = row.sub_id;
    console.log(id);
    for (const submission of submissions) {
      if (submission.id === id) {
        return submission;
      }
    }
    return null;
  }

  const allManualGraded = (selection: IRowValues[]) => {
    return selection.reduce((acc, cur) => {
      return cur.manual_status === "manually_graded" && acc
    }, true);
  }

  return (
    <div>
      <ModalTitle title="Grading">
      <Box sx={{ml: 2}} display="inline-block">
      <Tooltip title="Reload">
              <IconButton aria-label='reload' onClick={updateSubmissions}>
                <ReplayIcon />
              </IconButton>
              </Tooltip>
        </Box>
        </ModalTitle>
      <div style={{display: 'flex', height: '65vh', marginTop: '90px'}}>
        <div style={{flexGrow: 1}}>
          <DataGrid
            sx={{mb: 3, ml: 3, mr: 3}}
            columns={columns}
            rows={rows}
            checkboxSelection
            disableSelectionOnClick
            selectionModel={selectedRows}

            onSelectionModelChange={e => {
              const selectedIDs = new Set(e);
              const selectedRowData = rows.filter(row =>
                selectedIDs.has(row.id)
              );
              setSelectedRows(e);
              setSelectedRowsData(selectedRowData);
            }}
          />
        </div>
      </div>
      <span>
        <FormControl sx={{m: 3}}>
          <InputLabel id="submission-select-label">View</InputLabel>
          <Select
            labelId="submission-select-label"
            id="submission-select"
            value={option}
            label="Age"
            onChange={handleChange}
          >
            <MenuItem value={"all"}>All Submissions</MenuItem>
            <MenuItem value={"latest"}>Latest Submissions of Users</MenuItem>
          </Select>
        </FormControl>
        <Button
          disabled={selectedRows.length === 0}
          sx={{m: 3}}
          variant='outlined'
          onClick={handleAutogradeSubmissions}>
          {`Autograde ${selectedRows.length} selected`}
        </Button>
        <NavigateNextIcon
          color={(selectedRowsData.length === 1 && selectedRowsData[0]?.auto_status !== "automatically_graded")
            ? "error" : (selectedRowsData.length !== 1 || selectedRowsData[0]?.auto_status !== "automatically_graded")
              ? "disabled" : "primary"}
          sx={{mb: -1}}/>
        <Button
          disabled={(selectedRowsData.length !== 1 || selectedRowsData[0]?.auto_status !== "automatically_graded")}
          sx={{m: 3}}
          onClick={() => setDisplayManualGrading(true)}
          variant='outlined'>
          {`Manualgrade selected`}
        </Button>
        <NavigateNextIcon
          color={selectedRows.length === 0 ?
            "disabled" : allManualGraded(selectedRowsData)
              ? "primary" : "error"}
          sx={{mb: -1}}/>
        <Button
          disabled={selectedRows.length === 0 || !allManualGraded(selectedRowsData)}
          sx={{m: 3}}
          onClick={handleGenerateFeedback}
          variant='outlined'>
          {`Generate Feedback for ${selectedRows.length} selected`}
        </Button>
      </span>

      <LoadingOverlay
        onClose={onManualGradingClose}
        open={displayManualGrading}
        container={props.root}
        transition="zoom"
      >
        <ManualGrading lecture={props.lecture} assignment={props.assignment}
                       submission={getSubmissionFromRow(selectedRowsData[0])} username={selectedRowsData[0]?.username}/>
      </LoadingOverlay>

      {/* Dialog */}
      <AgreeDialog open={showDialog} {...dialogContent} />
      <Dialog
        open={showLogs}
        onClose={() => setShowLogs(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">
          {"Logs"}
        </DialogTitle>
        <DialogContent>
          <Typography id="alert-dialog-description" sx={{fontSize: 10, fontFamily: "'Roboto Mono', monospace"}}>
            {logs}
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowLogs(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};



