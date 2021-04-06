import * as React from 'react';
import { getAllAssignments } from '../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../model/assignment';
import { AssignmentComponent } from './assignment.component';

import { Icon } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

export interface AssignmentListProps {
  lectureId: number; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class AssignmentsComponent extends React.Component<AssignmentListProps> {
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
    return <div className="AssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">
        <Icon icon={IconNames.LEARNING} className="flavor-icon"></Icon>
        {this.title} 
        <Icon iconSize={Icon.SIZE_LARGE} icon={IconNames.CHEVRON_DOWN} className={`collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}`}></Icon> 
        </div>
      <Collapse isOpen={this.state.isOpen} className="collapse-body" transitionDuration={300} keepChildrenMounted={true}>
        <ul>
          {this.state.assignments.map((el, index) =>
            <AssignmentComponent index={index} lectureName={this.title} assignment={el} />
            )}
        </ul>
        
      </Collapse>
    </div>;
  }

}