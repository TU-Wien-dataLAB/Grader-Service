import { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import { DataGrid } from "@mui/x-data-grid";
import * as React from "react";
import { Assignment } from "../../model/assignment";
import { Lecture } from "../../model/lecture";
import { utcToLocalFormat } from "../../services/datetime.service";

export interface IGradingProps {
    lecture: Lecture;
    assignment: Assignment;
    latest_submissions: any;
}

export const GradingComponent = (props : IGradingProps) => {

    const generateRows = (submissions : any) => {
        let rows: any[] = [];
          submissions.forEach((sub : any) => {
            //get latest submission
            let latest = sub.submissions.reduce((a : any, b : any) => {
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
    } 
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
        ];
        
        const columns: GridColDef[] = [
          { field: 'col1', headerName: 'Column 1', width: 150 },
          { field: 'col2', headerName: 'Column 2', width: 150 },
        ];
    
  

    return (
        <div>
            <DataGrid columns={columns} rows={rows}></DataGrid>
        </div>
    );
}
