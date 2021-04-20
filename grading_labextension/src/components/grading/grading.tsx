import { Title, Widget } from '@lumino/widgets';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { fetchAssignment } from '../../services/assignments.service';
import { getLecture } from '../../services/lectures.service';
import { getAllSubmissions } from '../../services/submissions.service';
import { UserSubmissions } from '../../model/userSubmissions';

import { DataGrid, GridCellParams, GridColDef } from '@material-ui/data-grid';
import { Button } from '@blueprintjs/core/lib/cjs/components/button/buttons';

export interface GradingProps {
  lectureID: number;
  assignmentID: number;
  title: Title<Widget>;
}


export class GradingComponent extends React.Component<GradingProps> {
  public lectureID: number;
  public assignmentID: number;
  public title: Title<Widget>;

  public submissions: Submission[];
  public lectureId: number;
  public assignmentId: number;
  public columns: GridColDef[];
  public state = {
    assignment: {},
    lecture: {},
    submissions: new Array<UserSubmissions>(),
    isOpen: true,
    rows: new Array(),
  };


  constructor(props: GradingProps) {
    super(props);
    this.lectureID = props.lectureID;
    this.assignmentID = props.assignmentID;
    this.title = props.title;
    this.columns = [
      { field: 'id', headerName: 'Id', width: 100 },
      { field: 'user', headerName: 'User', width: 130 },
      { field: 'date', headerName: 'Date', width: 200 },
      {
        field: '',
        headerName: '',
        width: 150,
        disableClickEventBubbling: true,
        disableColumnMenu: true,
        renderCell: (params: GridCellParams) => (
            <Button icon="highlight" outlined>Autograde</Button>
        ),
      },
      { field: 'score', headerName: 'Score', width: 130 },

    ];
  }

  public async componentDidMount() {
    let assignment: Assignment = await fetchAssignment(this.lectureID, this.assignmentID, false, true).toPromise();
    let lecture: Lecture = await getLecture(this.lectureID).toPromise();
    this.title.label = "Grading: " + assignment.name;
    this.setState({ assignment, lecture })
    getAllSubmissions(lecture, assignment, false).subscribe(userSubmissions => {
      console.log(userSubmissions)
      this.setState(this.state.submissions = userSubmissions)
      //Temp rows for testing
      this.setState(this.state.rows = this.generateRows())
      console.log("rows:")
      console.log(this.state.rows)
    })
  }

  public generateRows(): Object[] {
    // let rows = [{ id: 10, user: "hasdf", date: "asdfadfa" }]
    let rows = new Array();
    //TODO: right now reading only the first 
    this.state.submissions.forEach( sub => {rows.push({id: sub.user.id, user: sub.user.name, date: sub.submissions[0].submitted_at})});
    return rows;
  }



  public render() {
    return (
        <div style={{ height: "100%",  display: "flex", flexDirection: "column"}}>
            <DataGrid rows={this.state.rows} columns={this.columns} checkboxSelection hideFooterPagination
             />
              <Button icon="highlight" color="primary" outlined style={{alignSelf: "flex-end", marginRight: "20px", marginBottom: "20px"}}>Autograde selected</Button>
        </div>
      
    );
  }
}