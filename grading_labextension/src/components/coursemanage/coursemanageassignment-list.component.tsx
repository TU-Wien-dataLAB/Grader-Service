import * as React from 'react';
import { createAssignment, getAllAssignments } from '../../services/assignments.service'
import { Collapse } from '@jupyterlab/ui-components'
import { Assignment } from '../../model/assignment';
import { CourseManageAssignmentComponent } from './coursemanageassignment.component';
import { Button, Icon } from '@blueprintjs/core';
import { showErrorMessage } from '@jupyterlab/apputils/lib/dialog';
import { InputDialog } from '@jupyterlab/apputils/lib/inputdialog';
import { Lecture } from '../../model/lecture';

export interface AssignmentListProps {
  lecture: Lecture; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class CourseManageAssignmentsComponent extends React.Component<AssignmentListProps> {
  public lecture: Lecture;
  public title: string;
  public state = {
    isOpen: false,
    assignments: new Array<Assignment>()
  };

  constructor(props: AssignmentListProps) {
    super(props)
    this.title = props.title
    this.lecture = props.lecture
    this.state.isOpen = props.open || false

    this.getAssignments = this.getAssignments.bind(this);


  }

  private async createAssignment() {
    try {
      let name;
      InputDialog.getText({title: 'Input assignment name'}).then(input => {
        name = input;
      })
      createAssignment(this.lecture.id, name);
    } catch (e) {
      showErrorMessage("Error Creating Assignment", e);
    }
  }


  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
  } 

  public componentDidMount() {
    this.getAssignments()
  }

  private getAssignments() {
    getAllAssignments(this.lecture.id).subscribe(assignments => {
      console.log(assignments)
      this.setState(this.state.assignments = assignments)
    })
  }



  public render() {
    return <div className="CourseManageAssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">
      <Icon icon="learning" className="flavor-icon"></Icon>
        <Icon icon="chevron-down" className={`collapse-icon ${this.state.isOpen ? "collapse-icon-open" : ""}`}></Icon>
        {this.title}

      </div>

      <Collapse isOpen={this.state.isOpen} className="collapse-body" keepChildrenMounted={true}>
        <ul>
          {this.state.assignments.map((el, index) =>
            <CourseManageAssignmentComponent index={index} lectureName={this.title} lecture={this.lecture} assignment={el} />
          )}
        </ul>
        <div className="assignment-create">       
         <Button icon="add" outlined onClick={this.createAssignment} className="assignment-button">Create new Assignment</Button>
        </div>
      </Collapse>
    </div>;
  }
}