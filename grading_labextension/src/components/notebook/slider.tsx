/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Button, Intent, Divider, Switch } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { CellWidget } from './create-assignment/cellwidget';
import { CellPlayButton } from './create-assignment/widget';
import { UserPermissions, Scope } from '../../services/permission.service';
import { GradeCellWidget } from './manual-grading/grade-cell-widget';
import { GradeCommentCellWidget } from './manual-grading/grade-comment-cell-widget';
import { getProperties, getSubmission, updateProperties, updateSubmission } from '../../services/submissions.service';
import { getAllLectures } from '../../services/lectures.service';
import { getAllAssignments } from '../../services/assignments.service';
import { GradeBook } from '../../services/gradebook';
import { Lecture } from '../../model/lecture';
import { Assignment } from '../../model/assignment';
import { showErrorMessage } from '@jupyterlab/apputils';
import { request } from '../../services/request.service';
export class NotebookModeSwitch extends ReactWidget {
  public ref: React.RefObject<SwitchComponent>;
  public component: JSX.Element;
  public mode: boolean;

  constructor(
    mode: boolean,
    notebookpanel: NotebookPanel,
    notebook: Notebook
  ) {
    super();
    this.mode = mode;
    const onChange = (m: boolean) => {
      this.mode = m;
    };

    this.component = (
      <SwitchComponent
        notebook={notebook}
        notebookpanel={notebookpanel}
        mode={mode}
        onChange={onChange}
      />
    );
  }

  protected render() {
    return this.component;
  }
}

export interface ImodeSwitchProps {
  mode: boolean;
  notebookpanel: NotebookPanel;
  notebook: Notebook;
  onChange: any;
}

export class SwitchComponent extends React.Component<ImodeSwitchProps> {
  public state = {
    mode: false,
    saveButtonText: "Save",
    transition: "show"
  };
  public notebook: Notebook;
  public notebookpanel: NotebookPanel;
  public lecture: Lecture;
  public assignment: Assignment;
  public gradeBook: GradeBook;
  public onChange: any;
  public isSourceNotebook: boolean;
  public hasPermissions: boolean;
  public isManualgradeNotebook: boolean;
  public subID: number;
  private notebookPaths: string[];
  private gradebook: GradeBook;

  public constructor(props: ImodeSwitchProps) {
    super(props);
    this.state.mode = props.mode || false;
    this.notebook = props.notebook;
    this.notebookpanel = props.notebookpanel;
    this.notebookPaths = this.notebookpanel.context.contentsModel.path.split("/")
    console.log("Notebook path: " + this.notebookpanel.context.contentsModel.path)
    this.isSourceNotebook = this.notebookPaths[0] === "source";
    this.isManualgradeNotebook = this.notebookPaths[0] === "manualgrade";
    this.hasPermissions = false;
    if (this.isManualgradeNotebook) {
      const lectureCode = this.notebookPaths[1]
      if (UserPermissions.getPermissions().hasOwnProperty(lectureCode)) {
        this.hasPermissions = UserPermissions.getPermissions()[lectureCode] !== Scope.student;
        this.subID = +this.notebookPaths[3]

      }
    }
    if (this.isSourceNotebook) {
      const lectureCode = this.notebookPaths[1]
      if (UserPermissions.getPermissions().hasOwnProperty(lectureCode)) {
        this.hasPermissions = UserPermissions.getPermissions()[lectureCode] !== Scope.student;
      }
    }

    console.log("Source notebook: " + this.isSourceNotebook);
    console.log("Creation mode permissions: " + this.hasPermissions);
    this.onChange = this.props.onChange;
    this.handleSwitchCreation = this.handleSwitchCreation.bind(this);
    this.handleSwitchGrading = this.handleSwitchGrading.bind(this);
  }

  public async componentDidMount() {
    const lectures = await getAllLectures().toPromise()
    this.lecture = lectures.find(l => l.code === this.notebookPaths[1])
    const assignments = await getAllAssignments(this.lecture.id).toPromise()
    this.assignment = assignments.find(a => a.name === this.notebookPaths[2])

    const properties = await getProperties(this.lecture.id, this.assignment.id, this.subID).toPromise()
    this.gradeBook = new GradeBook(properties);
  }

  public handleSwitchCreation = () => {
    this.setState({ mode: !this.state.mode }, () => {
      this.onChange(this.state.mode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.mode) {
          currentLayout.insertWidget(0, new CellWidget(c));
        } else {
          currentLayout.widgets.map(w => {
            if (w instanceof CellWidget) {
              currentLayout.removeWidget(w);
            }
          });
        }
        //old button remove
        currentLayout.widgets.map(w => {
          if (w instanceof CellPlayButton) {
            currentLayout.removeWidget(w);
          }
        });
      });
    });
  };

  public handleSwitchGrading = async () => {
    const properties = await getProperties(this.lecture.id, this.assignment.id, this.subID).toPromise()
    this.gradeBook = new GradeBook(properties);
    this.setState({ mode: !this.state.mode }, () => {
      this.onChange(this.state.mode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.mode) {
          currentLayout.insertWidget(0, new GradeCellWidget(c, this.gradeBook, this.notebookPaths[4].split(".").slice(0, -1).join(".")));
          currentLayout.addWidget(new GradeCommentCellWidget(c, this.gradeBook, this.notebookPaths[4].split(".").slice(0, -1).join(".")))
        } else {
          currentLayout.widgets.map(w => {
            if (w instanceof GradeCellWidget || w instanceof GradeCommentCellWidget) {
              currentLayout.removeWidget(w);
            }
          });
        }
      });
    });
  }

  private async saveProperties() {
    this.setState({ transition: "" })
    this.setState({ saveButtonText: "Saving" })
    try {
      await updateProperties(this.lecture.id, this.assignment.id, this.subID, this.gradeBook.properties);
      this.setState({ saveButtonText: "Saved" })
      //console.log("saved")
      setTimeout(() => this.setState({ saveButtonText: "Save", transition: "show" }), 2000);
      const submission = await getSubmission(this.lecture.id,this.assignment.id,this.subID).toPromise()
      console.log(submission)
      submission.manual_status = "manually_graded"
      updateSubmission(this.lecture.id,this.assignment.id,this.subID, submission)
    } catch (err) {
      this.setState({ saveButtonText: "Save", transition: "show" });
      showErrorMessage("Error saving properties", err);
    }
    

  }

  public render() {
    if (this.isSourceNotebook && this.hasPermissions) {
      return (
        <Switch
          checked={this.state.mode}
          label="Creationmode"
          onChange={this.handleSwitchCreation}
        />
      );
    } else if (this.isManualgradeNotebook && this.hasPermissions) {
      return (
        <span id="manual-grade-switch">
          <Switch
            checked={this.state.mode}
            label="Gradingmode"
            onChange={this.handleSwitchGrading}
          />
          <Button className="assignment-button" onClick={() => this.saveProperties()} icon={IconNames.FLOPPY_DISK} outlined intent={Intent.SUCCESS}>
            <span className={this.state.transition} >{this.state.saveButtonText}</span>
          </Button>
        </span>
      );
    }
    return null;
    // if the user has permissions it is also a source notebook

  }
}
