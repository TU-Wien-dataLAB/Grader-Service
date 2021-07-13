import { Button, Collapse, Icon, Tag } from '@blueprintjs/core';
import { Dialog, InputDialog, showDialog, showErrorMessage } from '@jupyterlab/apputils';
import * as React from 'react';
import { GlobalObjects } from '../../index';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { User } from '../../model/user';
import { getAllSubmissions } from '../../services/submissions.service';


export interface AssignmentProps {
  index: number;
  lectureName: string;
  assignment: Assignment;
  lecture: Lecture;
}


export class CourseManageAssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lectureName: string;
  public lecture: Lecture;
  public index: number;
  public iconSize: number = 14;
  public state = {
    isOpen: false,
    submissions: new Array<{user: User, submissions: Submission[]}>(),
  };


  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.assignment.id;
    this.lectureName = props.lectureName;
    this.lecture = props.lecture;
  }

  public componentDidMount() {
    if(this.assignment.status=="released") {
      getAllSubmissions(this.lecture , this.assignment,false,true).subscribe(userSubmissions => {
        this.setState(this.state.submissions = userSubmissions)
        console.log(this.state.submissions)
        console.log(this.state.submissions.length)
        } 
      )
    }
  }

  private toggleOpen = () => {
    console.log("toggle assignment header")
    this.setState({ isOpen: !this.state.isOpen });
  }

  private openFile(path: string) {
    console.log("Opening file: " + path)
    GlobalObjects.commands.execute('docmanager:open', {
      path: path,
      options: {
        mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
      }
    }).catch(error => {
      showErrorMessage("Error Opening File", error)
    })
  }

  private openGrading(lectureID: number, assignmentID: number) {
    GlobalObjects.commands.execute('grading:open', {
      lectureID,
      assignmentID
    }).catch(error => {
      showErrorMessage("Error Opening Submission View", error)
    })
  }

  private async openPreview() {
    //TODO: This should open the file in the preview directory not the /lecture/assignment directory
    let names = this.assignment.exercises.map(ex => ex.name);

    let path = `${this.lecture.name}/${this.assignment.name}/`;
    if (names.length > 1) {
      let value = await InputDialog.getItem({
        title: 'Choose an exercise to preview',
        items: names
      });
      if (value.value == null) return;
      path += value.value;
    } else {
      path += this.assignment.exercises[0].name;
    }

    GlobalObjects.commands.execute('docmanager:open', {
      path: path,
      options: {
        mode: 'split-right' // tab-after tab-before split-bottom split-right split-left split-top
      }
    }).catch(error => {
      showErrorMessage("Error Opening File", error)
    })
  }

  private async pushAssignment() {
    let result = await showDialog({
      title: "Push Assignment",
      body: `Do you want to push ${this.assignment.name}? This updates the state of the assignment on the server with your local state.`,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Push" })],
    });
    if (!result.button.accept) return;

    // TODO: push assignment

  }

  private async pullAssignment() {
    let result = await showDialog({
      title: "Pull Assignment",
      body: `Do you want to pull ${this.assignment.name}? This updates your assignment with the state of the server.`,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Pull" })],
    });
    if (!result.button.accept) return;

    // TODO: pull assignment
  }

  private async releaseAssignment() {
    let result = await showDialog({
      title: "Release Assignment",
      body: `Do you want to release ${this.assignment.name} for all students? This can NOT be undone!`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: "Release" })],
    });
    if (!result.button.accept) return;

    result = await showDialog({
      title: "Confirmation",
      body: `Are you sure you want to release ${this.assignment.name}?`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: "Release" })],
    });
    if (!result.button.accept) return;

    // TODO: release assignment
  }

  public render() {
    return <li key={this.index}>
      <div className="assignment">
        <div className="assignment-header">
          <span onClick={this.toggleOpen}>
            <Icon icon="chevron-right" iconSize={this.iconSize}
              className={`collapse-icon-small ${this.state.isOpen ? "collapse-icon-small-open" : ""}`}></Icon>
            <Icon icon="inbox" iconSize={this.iconSize} className="flavor-icon"></Icon>
            {this.assignment.name}
          </span>

          <span className="button-list">
            <Button icon='edit' outlined className="assignment-button">Edit</Button>
            <Button icon='search' outlined className="assignment-button" onClick={() => this.openPreview()} >Preview</Button>
            <Button icon='git-push' intent={"success"} outlined className="assignment-button" onClick={() => this.pushAssignment()} >Push</Button>
            <Button icon='git-pull' intent={"primary"} outlined className="assignment-button" onClick={() => this.pullAssignment()}> Pull</Button>
            <Button icon='cloud-upload' outlined className="assignment-button" disabled={this.assignment.status=="created"} onClick={() => this.releaseAssignment()} >Release</Button>
            <Tag className="assignment-tag" icon="arrow-top-right"  onClick={() => { this.openGrading(this.lecture.id, this.assignment.id)}}>{this.state.submissions.length} {"Submission" + ((this.state.submissions.length > 1) ?  "s" : "")}</Tag>
          </span>
        </div>

        <Collapse isOpen={this.state.isOpen}>
          <div className="assignment-content">
            {this.assignment.exercises.map((ex, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${ex.name}`)}>
                <Icon icon="edit" iconSize={this.iconSize} className="flavor-icon"></Icon>
                {ex.name}
              </div>
            )}

            {this.assignment.files.map((file, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${file.name}`)}>
                <Icon icon="document" iconSize={this.iconSize} className="flavor-icon"></Icon>
                {file.name}
              </div>
            )}
          </div>
        </Collapse>
      </div>
    </li>
  }
}
