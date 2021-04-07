import * as React from 'react';
import { getAllAssignments } from '../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../model/assignment';
import { AssignmentComponent } from './assignment.component';

import { Icon } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";
import { Lecture } from '../model/lecture';

export interface AssignmentListProps {
  lecture: Lecture;
  open?: boolean; // initial state of collapsable
}

export class AssignmentsComponent extends React.Component<AssignmentListProps> {
  public lecture: Lecture;
  public state = {
    isOpen: false,
    assignments: new Array<Assignment>()
  };

  constructor(props: AssignmentListProps) {
    super(props);
    this.lecture = props.lecture;
    this.state.isOpen = props.open || false;
  }

  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  public componentDidMount() {
    getAllAssignments(this.lecture.id).subscribe(assignments => {
      this.setState(this.state.assignments = assignments)
    })
  }

  public render() {
    return <div className="AssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">
        <Icon icon={IconNames.LEARNING} className="flavor-icon"></Icon>
        {this.lecture.name} 
        <Icon iconSize={Icon.SIZE_LARGE} icon={IconNames.CHEVRON_DOWN} className={`collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}`}></Icon> 
        </div>
      <Collapse isOpen={this.state.isOpen} className="collapse-body" transitionDuration={300} keepChildrenMounted={true}>
        <ul>
          {this.state.assignments.map((el, index) =>
            <AssignmentComponent index={index} lecture={this.lecture} assignment={el} />
            )}
        </ul>
      </Collapse>
    </div>;
  }

}