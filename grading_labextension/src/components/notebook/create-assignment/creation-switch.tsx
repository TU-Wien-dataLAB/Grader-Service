import { Button, Switch } from '@blueprintjs/core';
import { Cell } from '@jupyterlab/cells';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { PanelLayout } from "@lumino/widgets";
import React from 'react';
import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import { getAllAssignments } from '../../../services/assignments.service';
import { GradeBook } from '../../../services/gradebook';
import { getAllLectures } from '../../../services/lectures.service';
import { Scope, UserPermissions } from '../../../services/permission.service';
import { getProperties } from '../../../services/submissions.service';
import { ImodeSwitchProps } from "../slider";
import { CellWidget } from './cellwidget';
import { CellPlayButton } from './widget';

export class CreationModeSwitch extends React.Component<ImodeSwitchProps> {
    public state = {
        mode: false,
        saveButtonText: "Save",
        transition: "show"
      };
      protected notebook: Notebook;
      protected notebookpanel: NotebookPanel;
      public lecture: Lecture;
      public assignment: Assignment;
      public gradeBook: GradeBook;
      public onChange: any;
      public isSourceNotebook: boolean;
      public hasPermissions: boolean;
      public isManualgradeNotebook: boolean;
      public subID: number;
      public notebookPaths: string[];
    
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
      }
    
      public async componentDidMount() {
        const lectures = await getAllLectures().toPromise()
        this.lecture = lectures.find(l => l.code === this.notebookPaths[1])
        const assignments = await getAllAssignments(this.lecture.id).toPromise()
        this.assignment = assignments.find(a => a.name === this.notebookPaths[2])
    
        const properties = await getProperties(this.lecture.id, this.assignment.id, this.subID).toPromise()
        this.gradeBook = new GradeBook(properties);
      }
      
      
    protected handleChange = async () => {
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
    }

    public render() {
        return (
            <Switch
          checked={this.state.mode}
          label="Creationmode"
          onChange={this.handleChange}/>
        )
    }

    
}