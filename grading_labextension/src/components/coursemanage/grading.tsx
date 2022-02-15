import {DataGrid, GridRenderCellParams} from '@mui/x-data-grid';
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
  MenuItem, Typography
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


export interface IGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  latest_submissions: Submission[];
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
}

interface IRowValues {
  id: number,
  name: string,
  date: string,
  auto_status: string,
  manual_status: string,
  feedback_available: boolean,
  score: number
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

  const handleAutogradeSubmissions = async () => {
    setDialogContent({
      title: 'Autograde Selected Submissions',
      message: `Do you wish to autograde the seleceted submissions?`,
      handleAgree: async () => {
        try {
          const numSubs = selectedRows.length
          await Promise.all(selectedRows.map(async (row) => {
            await autogradeSubmission(props.lecture, props.assignment, row as Submission)
            console.log("Autograded submission");
          }));
          getAllSubmissions(props.lecture, props.assignment, false, true).then(response => {
            setRows(generateRows(response));
            props.showAlert('success', `Grading ${numSubs} Submissions`);
          })
        } catch (err) {
          console.error(err);
          props.showAlert('error', 'Error Autograding Submissions');
        }
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
          const numSubs = selectedRows.length
          await Promise.all(selectedRows.map(async (row) => {
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

    submissions.forEach((sub: Submission) => {
      rows.push({
        id: sub.id,
        name: sub.username,
        date: utcToLocalFormat(sub.submitted_at),
        auto_status: sub.auto_status,
        manual_status: sub.manual_status,
        feedback_available: sub.feedback_available,
        score: sub.score
      });
    });
    console.log(rows);
    return rows;
  };

  const [submissions, setSubmissions] = React.useState(props.latest_submissions);
  const [rows, setRows] = React.useState(generateRows(props.latest_submissions));
  const [selectedRows, setSelectedRows] = React.useState([] as IRowValues[]);

  const handleChange = (event: SelectChangeEvent) => {
    setOption(event.target.value as string);
  };

  React.useEffect(() => {
    const latest = option === 'latest' ? true : false;
    getAllSubmissions(props.lecture, props.assignment, latest, true).then(response => {
      setRows(generateRows(response));
      setSubmissions(response);
    })
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
    if (logs === undefined || logs === null) {
      logs = "No Logs Available!"
    }
    setLogs(logs);
    setShowLogs(true);
  }

  const columns = [
    {field: 'id', headerName: 'Id', width: 110},
    {field: 'name', headerName: 'User', width: 130},
    {field: 'date', headerName: 'Date', width: 170},
    {
      field: 'auto_status', headerName: 'Autograde-Status', width: 170,
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

  const getSubmissionFromRow = (row: IRowValues): Submission => {
    if (row === undefined) return null;
    const id = row.id;
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
      <ModalTitle title="Grading"/>
      <div style={{display: 'flex', height: '550px', marginTop: '90px'}}>
        <div style={{flexGrow: 1}}>
          <DataGrid
            sx={{mb: 3, ml: 3, mr: 3}}
            columns={columns}
            rows={rows}
            checkboxSelection
            disableSelectionOnClick
            onSelectionModelChange={e => {
              const selectedIDs = new Set(e);
              const selectedRowData = rows.filter(row =>
                selectedIDs.has(row.id)
              );
              setSelectedRows(selectedRowData);
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
          color={(selectedRows.length === 1 && selectedRows[0]?.auto_status !== "automatically_graded")
            ? "error" : (selectedRows.length !== 1 || selectedRows[0]?.auto_status !== "automatically_graded")
              ? "disabled" : "primary"}
          sx={{mb: -1}}/>
        <Button
          disabled={(selectedRows.length !== 1 || selectedRows[0]?.auto_status !== "automatically_graded")}
          sx={{m: 3}}
          onClick={() => setDisplayManualGrading(true)}
          variant='outlined'>
          {`Manualgrade selected`}
        </Button>
        <NavigateNextIcon
          color={selectedRows.length === 0 ?
            "disabled" : allManualGraded(selectedRows)
              ? "primary" : "error"}
          sx={{mb: -1}}/>
        <Button
          disabled={selectedRows.length === 0 || !allManualGraded(selectedRows)}
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
                       submission={getSubmissionFromRow(selectedRows[0])} username={selectedRows[0]?.name}/>
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



