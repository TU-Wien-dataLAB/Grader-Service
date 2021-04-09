import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { getAllSubmissions } from '../../services/submissions.service';
import { SubmissionComponent } from './gradingsubmission';
import { Table } from '@blueprintjs/table';


export interface CourseManageProps {
    lectureId: number;
    assignmentId: number;
}

export class CourseManageComponent extends React.Component<CourseManageProps> {
  public submissions: Submission[];
  public lectureId: number;
  public assignmentId: number;
  public state = {
    submissions: new Array<Submission>()
  };


  constructor(props: CourseManageProps) {
    super(props);
    this.lectureId = props.lectureId;
    this.assignmentId = props.assignmentId;

  }

  public componentDidMount() {
    getAllSubmissions(this.lectureId,this.assignmentId).subscribe(submissions => {
      console.log(submissions)
      this.setState(this.state.submissions = submissions)
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