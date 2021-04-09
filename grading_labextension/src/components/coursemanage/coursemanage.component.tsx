import * as React from 'react';
import { Lecture } from '../../model/lecture';
import { getAllLectures } from '../../services/lectures.service'
import { CourseManageAssignmentsComponent } from './coursemanageassignment-list.component';


export interface CourseManageProps {
  // lectures: Array<Lecture>;
}

export class CourseManageComponent extends React.Component<CourseManageProps> {
  public lectures: number[];
  public state = {
    lectures: new Array<Lecture>()
  };

  constructor(props: CourseManageProps) {
    super(props);
    // this.state = {"lectures": props.lectures};
  }

  public componentDidMount() {
    getAllLectures().subscribe(lectures => {
      console.log(lectures)
      this.setState(this.state.lectures = lectures)
    })
  }

  public render() {
    return <div className="course-list">
    {this.state.lectures.map((el, index) => <CourseManageAssignmentsComponent lecture={el} title={el.name} open={index==0} />)}
    </div>
   
  }
}