import { GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { DataGrid } from '@mui/x-data-grid';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { utcToLocalFormat } from '../../services/datetime.service';
import { Box, Button, Container, FormControl, Grid, InputLabel, MenuItem, Stack, Typography } from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { getAllSubmissions } from '../../services/submissions.service';

export interface IGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  latest_submissions: any;
}

export const GradingComponent = (props: IGradingProps) => {
  const [option, setOption] = React.useState('latest');


  const generateRows = (submissions: any) => {
    const rows: any[] = [];

    if (option === 'latest') {
      submissions.forEach((sub: any) => {
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
        sub.submissions.forEach((s : any) => {
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
    return rows;
  };

  const [rows, setRows] = React.useState(generateRows(props.latest_submissions));
  const [selectedRows, setselectedRows] = React.useState([]);

  const handleChange = (event: SelectChangeEvent) => {
    setOption(event.target.value as string);
    const latest = 'latest' === event.target.value;
    getAllSubmissions(props.lecture, props.assignment, latest, true).then(response => {
      setRows(generateRows(response))
      console.log(response)
    })
  };



  const columns = [
    { field: 'id', headerName: 'Id', width: 110 },
    { field: 'name', headerName: 'User', width: 130 },
    { field: 'date', headerName: 'Date', width: 170 },
    { field: 'auto_status', headerName: 'Autograde-Status', width: 170 },
    { field: 'manual_status', headerName: 'Manualgrade-Status', width: 170 },
    { field: 'score', headerName: 'Score', width: 130 }
  ];


  return (
    <Box>
      <ModalTitle title="Grading" />
      <Box>
        <DataGrid
          sx={{ minHeight: '600px' }}
          columns={columns}
          rows={rows}
          checkboxSelection
          disableSelectionOnClick
          onSelectionModelChange={e => {
            const selectedIDs = new Set(e);
            const selectedRowData = rows.filter(row =>
              selectedIDs.has(row.id)
            );
            setselectedRows(selectedRowData);

          }}
        />
      </Box>
      <FormControl>
        <InputLabel id="submission-select-label">View Submissions</InputLabel>
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
    </Box>
  );
};



export const ModalTitle = (props: any) => {
  return (
    <Box sx={{ m: 3, top: 4 }}>
      <Typography variant='h5'>
        {props.title}
      </Typography>
    </Box>
  )
}
