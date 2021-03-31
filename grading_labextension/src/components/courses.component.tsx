import * as React from 'react';
import { AssignmentsComponent } from './assignment-list.component';


export interface CoursesProps {
  lectures: number[];
}

export class CoursesComponent extends React.Component<CoursesProps> {
  public lectures: number[];
  public state = {
  };

  constructor(props: CoursesProps) {
    super(props)
    this.lectures = props.lectures
  }

  public render() {
    return <div className="course-list">
      {this.lectures.map((el, index) => <AssignmentsComponent aid={index} title={"Course " + index} open={index==0} />)}
    </div>
  }
}