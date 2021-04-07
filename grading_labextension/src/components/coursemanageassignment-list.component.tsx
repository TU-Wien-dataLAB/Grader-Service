import * as React from 'react';
import { createAssignment, getAllAssignments } from '../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../model/assignment';
import { CourseManageAssignmentComponent } from './coursemanageassignment.component';
import { Button, Icon } from '@blueprintjs/core';
import { showErrorMessage } from '@jupyterlab/apputils/lib/dialog';
import { InputDialog } from '@jupyterlab/apputils/lib/inputdialog';

export interface AssignmentListProps {
  lectureId: number; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class CourseManageAssignmentsComponent extends React.Component<AssignmentListProps> {
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

  private async createAssignment() {
    try {
      let name;
      InputDialog.getText({title: 'Input assignment name'}).then(input => {
        name = input;
      })
      createAssignment(this.lectureId, name);
    } catch (e) {
      showErrorMessage("Error Creating Assignment", e);
    }
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
        {this.title}

      </div>

      <Collapse isOpen={this.state.isOpen} className="collapse-body" keepChildrenMounted={true}>
        <ul>
          {this.state.assignments.map((el, index) =>
            <CourseManageAssignmentComponent index={index} lectureName={this.title} lectureId={this.lectureId} assignment={el} />
          )}
        </ul>
        <Button icon="add" outlined onClick={this.createAssignment} className="assignment-button">Create new Assignment</Button>
      </Collapse>
    </div>;
  }
}