import * as React from 'react';
import { getAllAssignments } from '../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../model/assignment';
import { AssignmentGradingComponent } from './gradingassignment.component';
import { Icon } from '@blueprintjs/core';

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
      <div onClick={this.toggleOpen} className="collapse-header">
      <Icon icon="chevron-down" className={`collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}`}></Icon> 
        {this.title} {this.state.isOpen ? "Edit Generate Preview Release Collect Submissions": ""}
      
</div>
      
      <Collapse isOpen={this.state.isOpen} className="collapse-body" keepChildrenMounted={true}>
        <ul>
          {this.state.assignments.map((el, index) =>
            <AssignmentGradingComponent index={index} lectureName={this.title} lectureId={this.lectureId} assignment={el} />
            )}
          </ul>
      </Collapse>
    </div>;
  }
}