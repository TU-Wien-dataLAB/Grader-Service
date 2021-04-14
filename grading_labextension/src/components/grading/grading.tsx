import { Title, Widget } from '@lumino/widgets';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { fetchAssignment } from '../../services/assignments.service';
import { getLecture } from '../../services/lectures.service';
import { getAllSubmissions } from '../../services/submissions.service';
import { UserSubmissions } from '../../model/userSubmissions';


import { DataGrid} from '@material-ui/data-grid';



const columns = [
  { field: 'User', headerName: 'Id', width: 100 },
  { field: 'firstName', headerName: 'First name', width: 130 },
  { field: 'lastName', headerName: 'Last name', width: 130 },
];

export interface GradingProps {
    lectureID: number;
    assignmentID: number;
    title: Title<Widget>;
}

const rows = [ {id: 123, firstname: "Florian", lastname: "Jäger"}, {id: 321, firstname: "Matthias", lastname: "Matt"}];


export class GradingComponent extends React.Component<GradingProps> {
  public lectureID: number;
  public assignmentID: number;
  public title: Title<Widget>;

  public submissions: Submission[];
  public lectureId: number;
  public assignmentId: number;
  public state = {
    assignment: {},
    lecture: {},
    submissions: new Array<UserSubmissions>(),
    isOpen: true,
  };


  constructor(props: GradingProps) {
    super(props);
    this.lectureID = props.lectureID;
    this.assignmentID = props.assignmentID;
    this.title = props.title;
  }

  public async componentDidMount() {
    let assignment: Assignment = await fetchAssignment(this.lectureID, this.assignmentID, false, true).toPromise();
    let lecture: Lecture = await getLecture(this.lectureID).toPromise();
    this.title.label = "Grading: " + assignment.name;
    this.setState({assignment, lecture})
    getAllSubmissions(lecture, assignment, false).subscribe(userSubmissions => {
      console.log(userSubmissions)
      this.setState(this.state.submissions = userSubmissions)
    })
  }

  

  public render() {
    return (
      <div style={{ height: 800, width: '100%' }}>
        <DataGrid rows={rows} columns={columns} pageSize={10} onRowSelected={ select => {}} checkboxSelection />
      </div>
    );
   
  }
}