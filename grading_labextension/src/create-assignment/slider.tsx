/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Button, Intent, Divider, Switch } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { CellWidget } from './cellwidget';
import { CellPlayButton } from './widget';
import { UserPermissions, Scope } from '../services/permission.service';
import { GradeCellWidget } from '../manual-grading/grade-cell-widget';
import { GradeCommentCellWidget } from '../manual-grading/grade-comment-cell-widget';
import { getProperties, updateProperties } from '../services/submissions.service';
import { getAllLectures } from '../services/lectures.service';
import { getAllAssignments } from '../services/assignments.service';
import { GradeBook } from '../services/gradebook';
import { Lecture } from '../model/lecture';
import { Assignment } from '../model/assignment';
export class CreationmodeSwitch extends ReactWidget {
  public ref: React.RefObject<CreationmodeSwitchComponent>;
  public component: JSX.Element;
  public mode: boolean;

  constructor(
    creationmode: boolean,
    notebookpanel: NotebookPanel,
    notebook: Notebook
  ) {
    super();
    this.mode = creationmode;
    const onChange = (m: boolean) => {
      this.mode = m;
    };

    this.component = (
      <CreationmodeSwitchComponent
        notebook={notebook}
        notebookpanel={notebookpanel}
        creationmode={creationmode}
        onChange={onChange}
      />
    );
  }

  protected render() {
    return this.component;
  }
}

export interface ICreationmodeSwitchProps {
  creationmode: boolean;
  notebookpanel: NotebookPanel;
  notebook: Notebook;
  onChange: any;
}

export class CreationmodeSwitchComponent extends React.Component<ICreationmodeSwitchProps> {
  public state = {
    creationmode: false,
    gradingmode: false,
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

  public constructor(props: ICreationmodeSwitchProps) {
    super(props);
    this.state.creationmode = props.creationmode || false;
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

  public handleSwitchCreation = () => {
    this.setState({ creationmode: !this.state.creationmode }, () => {
      this.onChange(this.state.creationmode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.creationmode) {
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
    //TODO: Bad calls that are switching everytime the switch is getting triggered
    //Move somewhere else
    const lectures = await getAllLectures().toPromise()
    this.lecture = lectures.find(l => l.code === this.notebookPaths[1])
    const assignments = await getAllAssignments(this.lecture.id).toPromise()
    this.assignment = assignments.find(a => a.name === this.notebookPaths[2])

    const properties = await getProperties(this.lecture.id, this.assignment.id, this.subID).toPromise()
    this.gradeBook = new GradeBook(properties);
    this.setState({ gradingmode: !this.state.gradingmode }, () => {
      this.onChange(this.state.gradingmode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.gradingmode) {
          currentLayout.insertWidget(0, new GradeCellWidget(c,this.gradeBook, this.notebookPaths[4].split(".").slice(0, -1).join(".")));
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
    console.log("saving properties");
    await updateProperties(this.lecture.id, this.assignment.id, this.subID, this.gradeBook.properties);
    console.log("saved");
  }

  public render() {
    if (this.isSourceNotebook && this.hasPermissions) {
      return (
        <Switch
          checked={this.state.creationmode}
          label="Creationmode"
          onChange={this.handleSwitchCreation}
        />
      );
    } else if (this.isManualgradeNotebook && this.hasPermissions) {
      return (
        <span id="manual-grade-switch">
          <Switch
            checked={this.state.gradingmode}
            label="Gradingmode"
            onChange={this.handleSwitchGrading}
          />
          <Button className="assignment-button" onClick={() => this.saveProperties()} icon={IconNames.FLOPPY_DISK} outlined intent={Intent.SUCCESS}>Save</Button>
        </span>
      );
    }
    return null;
    // if the user has permissions it is also a source notebook

  }
}
