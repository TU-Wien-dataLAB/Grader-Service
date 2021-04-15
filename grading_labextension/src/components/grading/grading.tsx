import { Title, Widget } from '@lumino/widgets';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { fetchAssignment } from '../../services/assignments.service';
import { getLecture } from '../../services/lectures.service';
import { getAllSubmissions } from '../../services/submissions.service';
import { UserSubmissions } from '../../model/userSubmissions';

import { DataGrid, GridColDef} from '@material-ui/data-grid';
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
      { field: 'Id', headerName: 'Id', width: 100 },
      { field: 'User', headerName: 'User', width: 130 },
      { field: 'Date', headerName: 'Date', width: 130 },
    ];
  }

  public async componentDidMount() {
    let assignment: Assignment = await fetchAssignment(this.lectureID, this.assignmentID, false, true).toPromise();
    let lecture: Lecture = await getLecture(this.lectureID).toPromise();
    this.title.label = "Grading: " + assignment.name;
    this.setState({assignment, lecture})
    getAllSubmissions(lecture, assignment, false).subscribe(userSubmissions => {
      console.log(userSubmissions)
      this.setState(this.state.submissions = userSubmissions)
      //Temp rows for testing
      this.setState(this.state.rows = this.generateRows())
    })
  }

  public generateRows() : Object[] {
    let rows = new Array();
    //TODO: right now reading only the first 
    this.state.submissions.forEach( sub => {rows.push({id: `${sub.user.id}`, user: `${sub.user.name}`, date: `${sub.submissions[0].submitted_at}`})});
    return rows;
  }

  

  public render() {
    return (
      <div style={{ height: 800, width: '100%' }}>
        <DataGrid rows={this.state.rows} columns={this.columns} onRowSelected={ select => {}} checkboxSelection />
      </div>
    );
   <Button icon="highlight" className="button-list" outlined />
  }
}