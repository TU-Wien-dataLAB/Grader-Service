import * as React from 'react';
import { AssignmentsComponent } from './assignment-list.component';
import { Lecture } from '../model/lecture';
import { getAllLectures } from '../services/lectures.service'

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
    console.log("Course component mounted!")
    getAllLectures().subscribe(lectures => {
      console.log(lectures)
      this.setState(this.state.lectures = lectures)
    })
  }

  public render() {
    return <div className="course-list">
      {this.state.lectures.map((el, index) => <AssignmentsComponent lect_id={el.id} title={el.name} open={index==0} />)}
    </div>
  }
}