import * as React from 'react';
import { getAllAssignments } from '../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../model/assignment';
import { AssignmentGradingComponent } from './gradingassignment.component';

export interface AssignmentListProps {
  lectureId: number; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class GradingAssignmentsComponent extends React.Component<AssignmentListProps> {
  public lectureId: number;
  public title: string;
  public state = {
    isOpen: false,
    assignments: new Array<Assignment>()
  };

  constructor(props: AssignmentListProps) {
    super(props)
    this.title = props.title
    this.lectureId = props.lectureId
    this.state.isOpen = props.open || false
  }

  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  public componentDidMount() {
    getAllAssignments(this.lectureId).subscribe(assignments => {
      console.log(assignments)
      this.setState(this.state.assignments = assignments)
    })
  }

  public render() {
    return <div className="GradingAssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">{this.title}</div>
      <Collapse isOpen={this.state.isOpen} className="collapse-body">
          {this.state.assignments.map((el, index) =>
            <AssignmentGradingComponent index={index} assignment={el} />
            )}
      </Collapse>
    </div>;
  }
}