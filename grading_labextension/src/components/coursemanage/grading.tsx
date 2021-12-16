import { GridColDef, GridRowsProp } from '@mui/x-data-grid';
import { DataGrid } from '@mui/x-data-grid';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { utcToLocalFormat } from '../../services/datetime.service';
import { Box, Typography } from '@mui/material';

export interface IGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  latest_submissions: any;
}

export const GradingComponent = (props: IGradingProps) => {
  const generateRows = (submissions: any) => {
    const rows: any[] = [];
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
      console.log(rows);
    });
    return rows;
  };
  /*
    const [rows,setRows] = React.useState(generateRows(props.latest_submissions));


    const columns = [
        { field: 'id', headerName: 'Id', width: 110 },
        { field: 'name', headerName: 'User', width: 130 },
        { field: 'date', headerName: 'Date', width: 170 },
        { field: 'auto_status', headerName: 'Autograde-Status', width: 170 },
        { field: 'manual_status', headerName: 'Manualgrade-Status', width: 170 },
        { field: 'score', headerName: 'Score', width: 130 }
        ];*/

  const rows: GridRowsProp = [
    { id: 1, col1: 'Hello', col2: 'World' },
    { id: 2, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 3, col1: 'MUI', col2: 'is Amazing' },
    { id: 4, col1: 'Hello', col2: 'World' },
    { id: 5, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 6, col1: 'MUI', col2: 'is Amazing' },
    { id: 7, col1: 'Hello', col2: 'World' },
    { id: 8, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 9, col1: 'MUI', col2: 'is Amazing' },
    { id: 10, col1: 'Hello', col2: 'World' },
    { id: 11, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 12, col1: 'MUI', col2: 'is Amazing' },
    { id: 13, col1: 'Hello', col2: 'World' },
    { id: 14, col1: 'DataGridPro', col2: 'is Awesome' },
    { id: 15, col1: 'MUI', col2: 'is Amazing' }
  ];

  const columns: GridColDef[] = [
    { field: 'col1', headerName: 'Column 1', width: 150 },
    { field: 'col2', headerName: 'Column 2', width: 150 }
  ];

  return (
    <Box sx={{ height: '85%' }}>
      <Typography sx={{ m: 3, top: 4 }} variant={'h5'}>
        Grading
      </Typography>
      <DataGrid sx={{ m: 4 }} columns={columns} rows={rows} />
    </Box>
  );
};
