import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { getAllSubmissions } from '../../services/submissions.service';
import { SubmissionComponent } from './gradingsubmission';


export interface CourseManageProps {
    lecture: Lecture;
    assignment: Assignment;
}

export class CourseManageComponent extends React.Component<CourseManageProps> {
  public submissions: Submission[];
  public state = {
    submissions: new Array<Submission>()
  };


  constructor(props: CourseManageProps) {
    super(props);

  }

  public componentDidMount() {
    getAllSubmissions({id:1},{id:1}).subscribe(submissions => {
      console.log(submissions)
      this.setState(this.state.submissions = submissions)
    })
  }

  public render() {
    return <div className="course-list">
    {this.state.submissions.map((el, index) => <SubmissionComponent />)}
    </div>
   
  }
}