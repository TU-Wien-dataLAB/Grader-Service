import * as React from 'react';
import { Assignment } from '../../model/assignment';

import { Icon, Collapse, Button, Intent } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { GlobalObjects } from '../../index';
import { showErrorMessage, showDialog, Dialog } from '@jupyterlab/apputils'
import { Submission } from '../../model/submission';
import { getAllSubmissions, submitAssignment } from '../../services/submissions.service'
import { fetchAssignment } from '../../services/assignments.service'
import { Lecture } from '../../model/lecture';

export interface AssignmentProps {
  index: number;
  lecture: Lecture;
  assignment: Assignment;
}

export class AssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lecture: Lecture;
  public index: number;
  public iconSize: number = 14;
  public state = {
    filesOpen: false,
    submissionsOpen: true,
    submissions: new Array<Submission>()
  };

  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
    this.lecture = props.lecture;

    this.toggleOpen = this.toggleOpen.bind(this);
    this.openFile = this.openFile.bind(this);
    this.fetchAssignment = this.fetchAssignment.bind(this);
    this.submitAssignment = this.submitAssignment.bind(this);
    this.getSubmissions = this.getSubmissions.bind(this);
  }

  public componentDidMount() {
    this.getSubmissions();
  }

  private toggleOpen = (collapsable: string) => {
    if (collapsable == "files") {
      this.setState({ filesOpen: !this.state.filesOpen });
    } else if (collapsable == "submissions") {
      this.setState({ submissionsOpen: !this.state.submissionsOpen })
    }
  }

  private async openFile(path: string) {
    if (this.assignment.status == 'released') { // if not fetched
      let result = await showDialog({
        title: "Assignment not fetched yet!",
        body: "Before working on assignments you need to fetch them! Do you want to fetch the assignment now?",
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Fetch Now" })]
      });
      if (!result.button.accept) {
        return;
      } else {
        await this.fetchAssignment();
      }
    }

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

  private async fetchAssignment() {
    try {
      let result = await showDialog({
        title: "Fetch Assignment",
        body: `Do you want to fetch ${this.assignment.name}?`,
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Fetch" })]
      })
      if (result.button.accept) {
        // update assignment
        this.assignment = await fetchAssignment(this.lecture.id, this.assignment.id).toPromise();
      }
    } catch (e) {
      showErrorMessage("Error Fetching Assignment", e);
    }
  }

  private async submitAssignment() {
    try {
      let result = await showDialog({
        title: "Submit Assignment",
        body: `Do you want to submit ${this.assignment.name}? You can always re-submit the assignment before the due date.`,
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: "Submit" })],
      })
      if (result.button.accept) {
        await submitAssignment(this.lecture, this.assignment).toPromise();
        await this.getSubmissions();
      }

    } catch (e) {
      showErrorMessage("Error Submitting Assignment", e);
    }
  }

  private getSubmissions() {
    getAllSubmissions(this.lecture, this.assignment).subscribe(
      submissions => this.setState({ submissions }),
      error => showErrorMessage("Error Loading Submissions", error)
    );
  }

  public render() {
    return <li key={this.index}>
      <div className="assignment">
        <div className="assignment-header">

          <Icon icon={IconNames.INBOX} iconSize={this.iconSize} className="flavor-icon"></Icon>
          {this.assignment.name}
          <span className="button-list">
            <Button className="assignment-button" onClick={this.fetchAssignment} icon={IconNames.CLOUD_DOWNLOAD} disabled={this.assignment.status != "released"} outlined intent={Intent.PRIMARY}>Fetch</Button>
            <Button className="assignment-button" onClick={this.submitAssignment} icon={IconNames.SEND_MESSAGE} disabled={this.assignment.status != "fetched"} outlined intent={Intent.SUCCESS}>Submit</Button>
          </span>

        </div>
        <div onClick={() => this.toggleOpen("files")} className="assignment-title">
          <Icon icon={IconNames.CHEVRON_RIGHT} iconSize={this.iconSize}
            className={`collapse-icon-small ${this.state.filesOpen ? "collapse-icon-small-open" : ""}`}></Icon>
          <Icon icon={IconNames.FOLDER_CLOSE} iconSize={this.iconSize} className="flavor-icon"></Icon>
          Exercises and Files
        </div>
        <Collapse isOpen={this.state.filesOpen}>
          <div className="assignment-content">
            {this.assignment.exercises.map((ex, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lecture.name}/${this.assignment.name}/${ex.name}`)}>
                <Icon icon={IconNames.EDIT} iconSize={this.iconSize} className="flavor-icon"></Icon>
                {ex.name}
              </div>
            )}

            {this.assignment.files.map((file, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lecture.name}/${this.assignment.name}/${file.name}`)}>
                <Icon icon={IconNames.DOCUMENT} iconSize={this.iconSize} className="flavor-icon"></Icon>
                {file.name}
              </div>
            )}
          </div>
        </Collapse>

        <div onClick={() => this.toggleOpen("submissions")} className="assignment-title">
          <Icon icon={IconNames.CHEVRON_RIGHT} iconSize={this.iconSize}
            className={`collapse-icon-small ${this.state.submissionsOpen ? "collapse-icon-small-open" : ""}`}></Icon>
          <Icon icon={IconNames.TICK_CIRCLE} iconSize={this.iconSize} className="flavor-icon"></Icon>
          Submissions
        </div>
        <Collapse isOpen={this.state.submissionsOpen}>
          <div className="assignment-content">
            {this.state.submissions.map((submission, i) =>
              <div className="submission-element" >
                <Icon icon={IconNames.FORM} iconSize={this.iconSize} className="flavor-icon"></Icon>
                {submission.submitted_at}
                {submission.status != "not_graded" ?
                  <Button className="assignment-button" icon={IconNames.CLOUD_DOWNLOAD} active={true} outlined={true} intent={Intent.PRIMARY} small={true}>
                    Fetch Feedback
                  </Button>
                  : null}
              </div>
            )}
          </div>
        </Collapse>
      </div>
    </li>
  }
}
