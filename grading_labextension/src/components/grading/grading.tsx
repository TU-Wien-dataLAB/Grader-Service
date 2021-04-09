import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { getAllSubmissions } from '../../services/submissions.service';
import { SubmissionComponent } from './gradingsubmission';
import { Table,Cell,Column } from '@blueprintjs/table';
import { Button } from '@blueprintjs/core/lib/cjs/components/button/buttons';


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
    /*getAllSubmissions(this.lectureId,this.assignmentId).subscribe(submissions => {
      console.log(submissions)
      this.setState(this.state.submissions = submissions)
    })*/
  }

  public render() {
    const userid = () => <Cell>{`${this.state.submissions}`}</Cell>;
    const autograde = () => <Cell><Button icon="automatic-updates">Autograde</Button></Cell>
    const score = () => <Cell></Cell>; //TODO:

    return <div className="course-list">
        <Table numRows={this.state.submissions.length}>
            <Column name="Users" cellRenderer={userid}></Column>
            <Column name="Autograde" cellRenderer={autograde}></Column>
            <Column name="Score" cellRenderer={score}></Column>
        </Table>
    </div>
   
  }
}