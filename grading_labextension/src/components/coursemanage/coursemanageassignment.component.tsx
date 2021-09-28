import { Button, Collapse, Icon, Tag } from '@blueprintjs/core';
import { Dialog, showDialog, showErrorMessage } from '@jupyterlab/apputils';
import * as React from 'react';
import { GlobalObjects } from '../../index';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { User } from '../../model/user';
import { getAllSubmissions } from '../../services/submissions.service';
import {
  deleteAssignment,
  generateAssignment,
  pullAssignment,
  pushAssignment,
  updateAssignment
} from '../../services/assignments.service';
import { InputDialog } from './coursemanageassignment-list.component';
import { InputDialog as LabInputDialog } from '@jupyterlab/apputils/lib/inputdialog';
import { DirListing } from '@jupyterlab/filebrowser/lib/listing';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { ExistingNodeRenderer } from '../assignments/assignment.component';
import { ITerminal } from '@jupyterlab/terminal';
import { Terminal } from '@jupyterlab/services';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { localToUTC } from '../../services/datetime.service';
import { Contents } from '@jupyterlab/services';
import moment from 'moment';

export interface AssignmentProps {
  parentUpdate: () => void;
  index: number;
  lectureName: string;
  assignment: Assignment;
  lecture: Lecture;
  assignments: Assignment[];
}

export interface AssignmentState {
  isOpen: boolean;
  submissions: { user: User; submissions: Submission[] }[];
  assignment: Assignment;
  showSource: boolean;
  transition: string;
}

export class CourseManageAssignmentComponent extends React.Component<
  AssignmentProps,
  AssignmentState
> {
  public parentUpdate: () => void;
  public lectureName: string;
  public lecture: Lecture;
  public index: number;
  public iconSize: number = 14;
  public state = {
    isOpen: false,
    submissions: new Array<{ user: User; submissions: Submission[] }>(),
    assignment: {} as Assignment,
    showSource: true,
    transition: "show",
  };
  public dirListingNode: HTMLElement;
  public dirListing: DirListing;
  public terminalSession: Terminal.ITerminalConnection = null;

  private generationTimestamp: number = null;
  private sourceChangeTimestamp: number = moment().valueOf(); // now

  constructor(props: AssignmentProps) {
    super(props);
    this.parentUpdate = props.parentUpdate;
    this.state.assignment = props.assignment;
    this.index = props.assignment.id;
    this.lectureName = props.lectureName;
    this.lecture = props.lecture;
  }

  public async componentDidMount() {
    if (this.state.assignment.status == 'released') {
      getAllSubmissions(
        this.lecture,
        this.state.assignment,
        false,
        true
      ).subscribe(userSubmissions => {
        this.setState({ submissions: userSubmissions });
        console.log(this.state.submissions);
        console.log(this.state.submissions.length);
      });
    }
    console.log('dirListingNode: ' + this.dirListingNode);
    const renderer = new ExistingNodeRenderer(this.dirListingNode);
    const model = new FilterFileBrowserModel({
      auto: true,
      manager: GlobalObjects.docManager
    });

    const LISTING_CLASS = 'jp-FileBrowser-listing';
    this.dirListing = new DirListing({ model, renderer });
    this.dirListing.addClass(LISTING_CLASS);
    const srcPath = `source/${this.lecture.code}/${this.state.assignment.name}`
    await model.cd(srcPath);
    this.dirListingNode.onclick = async ev => {
      const model = this.dirListing.modelForClick(ev);
      if (model == undefined) {
        this.dirListing.handleEvent(ev);
        return;
      }
      if (!this.dirListing.isSelected(model.name)) {
        await this.dirListing.selectItemByName(model.name);
      } else {
        this.dirListing.clearSelectedItems();
        this.dirListing.update();
      }
    };
    this.dirListingNode.ondblclick = ev => {
      const model = this.dirListing.modelForClick(ev);
      this.openFile(model.path);
    };
    this.dirListingNode.oncontextmenu = ev => {
      ev.preventDefault();
      ev.stopPropagation();
    };

    GlobalObjects.docManager.services.contents.fileChanged.connect((
      sender: Contents.IManager,
      change: Contents.IChangedArgs
    ) => {
      const { oldValue, newValue } = change;
      if (!newValue.path.includes(srcPath)) {
        return;
      }

      const modified = moment(newValue.last_modified).valueOf()
      if (this.sourceChangeTimestamp === null || this.sourceChangeTimestamp < modified) {
        this.sourceChangeTimestamp = modified
      }
      console.log("New source file changed timestamp: " + this.sourceChangeTimestamp)
    }, this)
  }

  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
    this.dirListing.update();
  };

  private async openTerminal() {
    const path = `~/${this.getRootDir(this.state.showSource)}/${this.lecture.code
      }/${this.state.assignment.name}`;
    console.log('Opening terminal at: ' + path.replace(' ', '\\ '));
    let args = {};
    if (
      this.terminalSession !== null &&
      this.terminalSession.connectionStatus === 'connected'
    ) {
      args = { name: this.terminalSession.name };
    }
    const main = (await GlobalObjects.commands.execute(
      'terminal:open',
      args
    )) as MainAreaWidget<ITerminal.ITerminal>;

    if (main) {
      const terminal = main.content;
      this.terminalSession = terminal.session;
    }

    try {
      this.terminalSession.send({
        type: 'stdin',
        content: ['cd ' + path.replace(' ', '\\ ') + '\n']
      });
    } catch (e) {
      console.error(e);
      main.dispose();
    }
  }

  private async openBrowser() {
    const path = `${this.getRootDir(this.state.showSource)}/${this.lecture.code
      }/${this.state.assignment.name}`;
    GlobalObjects.commands
      .execute('filebrowser:go-to-path', {
        path
      })
      .catch(error => {
        showErrorMessage('Error showing in File Browser', error);
      });
  }

  private async switchRoot() {
    this.setState({ transition: "hide" })
    if (this.state.showSource) {
      // TODO: check if source files have actually changed before generating
      if (this.generationTimestamp === null || this.generationTimestamp < this.sourceChangeTimestamp) {
        // switching to release
        await generateAssignment(this.lecture.id, this.state.assignment).toPromise();
        this.generationTimestamp = moment().valueOf();
      }
    }
    let path = `/${this.getRootDir(!this.state.showSource)}/${this.lecture.code
      }/${this.state.assignment.name}`;
    await this.dirListing.model.cd(path);
    this.setState({ showSource: !this.state.showSource, transition: "show" });
  }

  private openFile(path: string) {
    console.log('Opening file: ' + path);
    GlobalObjects.commands
      .execute('docmanager:open', {
        path: path,
        options: {
          mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
        }
      })
      .catch(error => {
        showErrorMessage('Error Opening File', error);
      });
  }

  private openGrading(lectureID: number, assignmentID: number) {
    GlobalObjects.commands
      .execute('grading:open', {
        lectureID,
        assignmentID
      })
      .catch(error => {
        showErrorMessage('Error Opening Submission View', error);
      });
  }

  private getRootDir(source: boolean): string {
    return source ? 'source' : 'release';
  }

  private async pushAssignment() {
    const result = await showDialog({
      title: 'Push Assignment',
      body: `Do you want to push ${this.state.assignment.name}? This updates the state of the assignment on the server with your local state.`,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Push' })]
    });
    if (!result.button.accept) {
      return;
    }

    await pushAssignment(this.lecture.id, this.state.assignment.id, 'source').toPromise();
    pushAssignment(this.lecture.id, this.state.assignment.id, 'release');
  }

  private async pullAssignment() {
    const result = await showDialog({
      title: 'Pull Assignment',
      body: `Do you want to pull ${this.state.assignment.name}? This updates your assignment with the state of the server and overwrites all changes.`,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Pull' })]
    });
    if (!result.button.accept) {
      return;
    }

    await pullAssignment(this.lecture.id, this.state.assignment.id, 'source').toPromise();
    this.dirListing.update();
  }

  private async releaseAssignment() {
    let result = await showDialog({
      title: 'Release Assignment',
      body: `Do you want to release ${this.state.assignment.name} for all students?`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: 'Release' })]
    });
    if (!result.button.accept) {
      return;
    }

    result = await showDialog({
      title: 'Confirmation',
      body: `Are you sure you want to release ${this.state.assignment.name}?`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: 'Release' })]
    });
    if (!result.button.accept) {
      return;
    }

    this.state.assignment.status = 'released';
    updateAssignment(this.lecture.id, this.state.assignment).subscribe(a =>
      this.setState({ assignment: a })
    );
  }

  private async withholdAssignment() {
    let result = await showDialog({
      title: 'Withhold Assignment',
      body: `Do you want to withhold ${this.state.assignment.name} for all students?`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: 'Withold' })]
    });
    if (!result.button.accept) {
      return;
    }

    result = await showDialog({
      title: 'Confirmation',
      body: `Are you sure you want to withold ${this.state.assignment.name}?`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: 'Withold' })]
    });
    if (!result.button.accept) {
      return;
    }

    this.state.assignment.status = 'created';
    updateAssignment(this.lecture.id, this.state.assignment).subscribe(a =>
      this.setState({ assignment: a })
    );
  }

  private async createFile(notebook = true) {
    let result: Dialog.IResult<string>;
    let filename = ';';
    if (notebook) {
      result = await InputDialog.getText({ title: 'Notebook name' });

      filename = result.value + '.ipynb';
    } else {
      result = await InputDialog.getText({ title: 'Filename with extension' });
      filename = result.value;
    }
    if (!result.button.accept) {
      return;
    }
    console.log('Create file: ' + filename);
    GlobalObjects.docManager.createNew(
      `source/${this.lecture.code}/${this.state.assignment.name}/${filename}`
    );
    this.dirListing.update();
  }

  private async delete() {
    const result = await showDialog({
      title: 'Release Assignment',
      body: `Do you want to delete ${this.state.assignment.name}? This can NOT be undone!`,
      buttons: [Dialog.cancelButton(), Dialog.warnButton({ label: 'Delete' })]
    });
    if (!result.button.accept) {
      return;
    }

    await deleteAssignment(this.lecture.id, this.state.assignment.id).toPromise();
    this.props.assignments.filter(a => a.id != this.state.assignment.id);
    this.parentUpdate();
  }

  private async editAssignment() {
    const name: Dialog.IResult<string> = await LabInputDialog.getText({
      title: 'Assignment name',
      placeholder: this.state.assignment.name
    });
    if (!name.button.accept) {
      return;
    }
    const date: Dialog.IResult<string> = await InputDialog.getDate({
      title: 'Input Deadline'
    });
    if (!date.button.accept) {
      return;
    }
    const type: Dialog.IResult<string> = await LabInputDialog.getItem({
      title: 'Assignment Type',
      items: ['user', 'group'],
      current: this.state.assignment.type === Assignment.TypeEnum.User ? 0 : 1
    });
    if (!type.button.accept) {
      return;
    }

    if (date.value === '') {
      this.state.assignment.due_date = null;
    } else {
      this.state.assignment.due_date = localToUTC(date.value);
    }

    if (type.value === 'user') {
      this.state.assignment.type = Assignment.TypeEnum.User;
    } else {
      this.state.assignment.type = Assignment.TypeEnum.Group;
    }

    if (name.value !== '') {
      this.state.assignment.name = name.value;
    }

    updateAssignment(this.lecture.id, this.state.assignment).subscribe(
      assignment => {
        this.setState({ assignment });
      }
    );
  }

  private async generateAssignment() {
    const result = await showDialog({
      title: 'Generate Assignment',
      body: `Do you want to generate ${this.state.assignment.name}? This create a local student-version preview in the release folder.`,
      buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Generate' })]
    });
    if (!result.button.accept) {
      return;
    }
    generateAssignment(this.lecture.id, this.state.assignment)
    this.dirListing.update()
  }


  public assignment() {
    return (
      <li key={this.index}>
        <div className={
          'assignment'    //bp3-card bp3-elevation-2
        }>
          <div className="assignment-header">
            <span onClick={this.toggleOpen} className="flex-item">
              <Icon
                icon="chevron-right"
                iconSize={this.iconSize}
                className={`collapse-icon-small ${this.state.isOpen ? 'collapse-icon-small-open' : ''
                  }`}
              ></Icon>
              <Icon
                icon="inbox"
                iconSize={this.iconSize}
                className="flavor-icon"
              ></Icon>
              {this.state.assignment.name}{' '}
              {this.state.showSource ? 'Source' : 'Release'} Files
            </span>

            <span className="button-list flex-item">
              <Button
                icon="edit"
                outlined
                className="assignment-button"
                onClick={() => this.editAssignment()}
              >
                Edit
              </Button>
              <Button
                icon="map-create"
                outlined
                className="assignment-button"
                onClick={() => this.generateAssignment()}
              >
                Generate
              </Button>
              <Button
                icon="git-push"
                intent={'success'}
                outlined
                className="assignment-button"
                onClick={() => this.pushAssignment()}
              >
                Push
              </Button>
              <Button
                icon="git-pull"
                intent={'primary'}
                outlined
                className="assignment-button"
                onClick={() => this.pullAssignment()}
              >
                {' '}
                Pull
              </Button>

              <Button
                icon="cloud-upload"
                outlined
                className="assignment-button"
                intent={this.state.assignment.status == "released" ? "danger" : "none"}
                onClick={this.state.assignment.status == "released" ? 
                 () => this.withholdAssignment()
                 : () => this.releaseAssignment()}>
                  {this.state.assignment.status == "released" ? "Withhold" : "Release"}
                </Button> 
                  

              
              <Button
                icon="arrow-top-right"
                intent="primary"
                outlined
                className="assignment-button"
                onClick={() => {
                  this.openGrading(this.lecture.id, this.state.assignment.id);
                }}
              >
                {this.state.submissions.length}{' '}
                {'Submission' + (this.state.submissions.length > 1 ? 's' : '')}
              </Button>
              <Button
                icon="delete"
                intent="danger"
                outlined
                className="assignment-button"
                onClick={() => this.delete()}
              >
                Delete
              </Button>
            </span>
          </div>

          <Collapse isOpen={this.state.isOpen} keepChildrenMounted={true}>
            <div
              className="assignment-dir-listing"
              ref={_element => (this.dirListingNode = _element)}
            ></div>
            <Button
              icon="add"
              outlined
              onClick={() => this.createFile(true)}
              className="assignment-button"
            >
              Add Notebook
            </Button>
            <Button
              icon="console"
              outlined
              onClick={() => this.openTerminal()}
              className="assignment-button"
            >
              Open in Terminal
            </Button>
            <Button
              icon="folder-open"
              outlined
              onClick={() => this.openBrowser()}
              className="assignment-button"
            >
              Reveal in File Browser
            </Button>
            <Button
              icon="switch"
              intent={this.state.showSource ? "none" : "primary"}
              outlined
              onClick={() => this.switchRoot()}
              className="assignment-button"
            >
              Switch to {!this.state.showSource ? 'Source' : 'Release'} View
            </Button>
          </Collapse>
        </div>
      </li>
    );
  }
  public render() {
    return (
      <div className={this.state.transition}>
        {this.assignment()}
      </div>
    );
  }
}
