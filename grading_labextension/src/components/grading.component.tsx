import * as React from 'react';
import { Lecture } from '../model/lecture';
import { getAllLectures } from '../services/lectures.service'
import { GradingAssignmentsComponent } from './gradingassignment-list.component';


export interface GradingProps {
  // lectures: Array<Lecture>;
}

export class GradingComponent extends React.Component<GradingProps> {
  public lectures: number[];
  public state = {
    lectures: new Array<Lecture>()
  };

  constructor(props: GradingProps) {
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
    return <div className="grading">
    {this.state.lectures.map((el, index) => <GradingAssignmentsComponent lectureId={el.id} title={el.name} open={index==0} />)}
    </div>
   
  }
}