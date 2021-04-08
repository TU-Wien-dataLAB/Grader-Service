import * as React from 'react';
import { AssignmentsComponent } from './assignment-list.component';
import { Lecture } from '../../model/lecture';
import { getAllLectures } from '../../services/lectures.service'
import { showErrorMessage } from '@jupyterlab/apputils'

export interface CoursesProps {
  // lectures: Array<Lecture>;
}

export class CoursesComponent extends React.Component<CoursesProps> {
  public lectures: number[];
  public state = {
    lectures: new Array<Lecture>()
  };

  constructor(props: CoursesProps) {
    super(props);
    // this.state = {"lectures": props.lectures};
  }

  public componentDidMount() {
    getAllLectures().subscribe(
      lectures => this.setState(this.state.lectures = lectures),
      error => showErrorMessage("Error Fetching Lectures", error))
  }

  public render() {
    return <div className="course-list">
      {this.state.lectures.map((el, index) => <AssignmentsComponent lecture={el} open={index==0} />)}
    </div>
  }
}