import {DataGrid} from '@mui/x-data-grid';
import * as React from 'react';
import {Assignment} from '../../model/assignment';
import {Lecture} from '../../model/lecture';
import {utcToLocalFormat} from '../../services/datetime.service';
import {AlertProps, Button, FormControl, InputLabel, MenuItem, Portal, Snackbar} from '@mui/material';
import Select, {SelectChangeEvent} from '@mui/material/Select';
import {getAllSubmissions} from '../../services/submissions.service';
import {AgreeDialog} from './dialog';
import MuiAlert from '@mui/material/Alert';
import {ModalTitle} from "../util/modal-title";
import {User} from "../../model/user";
import {Submission} from "../../model/submission";
import {autogradeSubmission} from "../../services/grading.service";


export interface IGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  latest_submissions: any;
}

interface IRowValues {
  id: number,
  name: string,
  date: string,
  auto_status: string,
  manual_status: string,
  score: number
}

export const GradingComponent = (props: IGradingProps) => {
  const [option, setOption] = React.useState('latest');
  //TODO: We have redundant code with AgreeDialog, maybe there is a way to put all states in a different component for example
  const [alert, setAlert] = React.useState(false);
  const [severity, setSeverity] = React.useState('success');
  const [alertMessage, setAlertMessage] = React.useState('');
  const [showDialog, setShowDialog] = React.useState(false);
  const [dialogContent, setDialogContent] = React.useState({
    title: '',
    message: '',
    handleAgree: null,
    handleDisagree: null
  });


  const showAlert = (severity: string, msg: string) => {
    setSeverity(severity);
    setAlertMessage(msg);
    setAlert(true);
  };

  const handleAutogradeSubmissions = async () => {
    setDialogContent({
      title: 'Autograde Selected Submissions',
      message: ``,
      handleAgree: async () => {
        try {
          const numSubs = selectedRows.length
          await Promise.all(selectedRows.map(async (row) => {
            await autogradeSubmission(props.lecture, props.assignment, row as Submission)
            console.log("Autograded submission");
          }));
          getAllSubmissions(props.lecture, props.assignment, false, true).then(response => {
            setRows(generateRows(response));
            showAlert('success', `Grading ${numSubs} Submissions`);
          })
        } catch (err) {
          console.error(err);
          showAlert('error', 'Error Autograding Submissions');
        }
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  const closeDialog = () => setShowDialog(false);

  const handleAlertClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === 'clickaway') {
      return;
    }
    setAlert(false);
  };

  const generateRows = (submissions: { user: User, submissions: Submission[] }[]) => {
    console.log("Submissions");
    console.log(submissions);
    console.log("option: " + option);
    const rows: IRowValues[] = [];

    if (option === 'latest') {
      submissions.forEach(sub => {
        //get latest submission
        const latest = sub.submissions.reduce((a: any, b: any) => {
          return new Date(a.submitted_at) > new Date(b.submitted_at) ? a : b;
        });
        rows.push({
          id: latest.id,
          name: sub.user.name,
          date: utcToLocalFormat(latest.submitted_at),
          auto_status: latest.auto_status,
          manual_status: latest.manual_status,
          score: latest.score
        });
      });

    } else {
      submissions.forEach((sub: any) => {
        sub.submissions.forEach((s: any) => {
          rows.push({
            id: s.id,
            name: sub.user.name,
            date: utcToLocalFormat(s.submitted_at),
            auto_status: s.auto_status,
            manual_status: s.manual_status,
            score: s.score
          });
        });
      });
    }
    console.log(rows);
    return rows;
  };

  const [rows, setRows] = React.useState(generateRows(props.latest_submissions));
  const [selectedRows, setSelectedRows] = React.useState([] as IRowValues[]);

  const handleChange = (event: SelectChangeEvent) => {
    setOption(event.target.value as string);
  };

  React.useEffect(() => {
    getAllSubmissions(props.lecture, props.assignment, false, true).then(response => {
      setRows(generateRows(response))
    })
  }, [option]);


  const columns = [
    {field: 'id', headerName: 'Id', width: 110},
    {field: 'name', headerName: 'User', width: 130},
    {field: 'date', headerName: 'Date', width: 170},
    {field: 'auto_status', headerName: 'Autograde-Status', width: 170},
    {field: 'manual_status', headerName: 'Manualgrade-Status', width: 170},
    {field: 'score', headerName: 'Score', width: 130}
  ];


  return (
    <div>
      <ModalTitle title="Grading"/>
      <div style={{display: 'flex', height: '500px'}}>
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
      <Button sx={{m: 3}} variant='outlined'>Generate Feedback of selected</Button>
      </span>

      {/* Dialog */}
      <AgreeDialog open={showDialog} {...dialogContent} />
      <Portal container={document.body}>
        <Snackbar
          open={alert}
          autoHideDuration={3000}
          onClose={handleAlertClose}
          sx={{mb: 2, ml: 2}}
        >
          <MuiAlert
            onClose={handleAlertClose}
            severity={severity as AlertProps['severity']}
            sx={{width: '100%'}}
          >
            {alertMessage}
          </MuiAlert>
        </Snackbar>
      </Portal>

    </div>
  );
};



