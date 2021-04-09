import { Title, Widget } from '@lumino/widgets';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { fetchAssignment } from '../../services/assignments.service';
import { getLecture } from '../../services/lectures.service';
import { getAllSubmissions } from '../../services/submissions.service';
import { SubmissionComponent } from './gradingsubmission';
import { Table } from '@blueprintjs/table';


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
  public state = {
    assignment: {},
    lecture: {},
    submissions: new Array<Submission>(),
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
    getAllSubmissions(lecture, assignment, false, true).subscribe(userSubmissions => {
      console.log(userSubmissions)
      this.setState(this.state.submissions = userSubmissions.submissions)
    })
  }

  public render() {
    return <div className="course-list">
        <Table numRows={2}>
    {this.state.submissions.map((sub, index) => <SubmissionComponent />)}
    </Table>
    </div>
   
  }
}