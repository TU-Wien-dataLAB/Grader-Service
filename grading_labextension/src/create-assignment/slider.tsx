/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Switch } from '@blueprintjs/core';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { CellWidget } from './cellwidget';
import { CellPlayButton } from './widget';
import { UserPermissions, Scope } from '../services/permission.service';
import { GradeCellWidget } from '../manual-grading/grade-cell-widget';

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
  public onChange: any;
  public isSourceNotebook: boolean;
  public hasPermissions: boolean;
  public isManualgradeNotebook: boolean;

  public constructor(props: ICreationmodeSwitchProps) {
    super(props);
    this.state.creationmode = props.creationmode || false;
    this.notebook = props.notebook;
    this.notebookpanel = props.notebookpanel;
    const notebookPaths: string[] = this.notebookpanel.context.contentsModel.path.split("/")
    console.log("Notebook path: " + this.notebookpanel.context.contentsModel.path)
    this.isSourceNotebook = notebookPaths[0] === "source";
    this.isManualgradeNotebook = notebookPaths[0] === "manualgrade";
    this.hasPermissions = false;
    if (this.isManualgradeNotebook) {
      const lectureCode = notebookPaths[1]
      if (UserPermissions.getPermissions().hasOwnProperty(lectureCode)) {
        this.hasPermissions = UserPermissions.getPermissions()[lectureCode] !== Scope.student;
      }
    }
    if (this.isSourceNotebook) {
      const lectureCode = notebookPaths[1]
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

  public handleSwitchGrading = () => {
    this.setState({ gradingmode: !this.state.gradingmode }, () => {
      this.onChange(this.state.gradingmode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.gradingmode) {
          currentLayout.insertWidget(0, new GradeCellWidget(c));
        } else {
          currentLayout.widgets.map(w => {
            if (w instanceof GradeCellWidget) {
              currentLayout.removeWidget(w);
            }
          });
        }
      });
    });
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
        <Switch
          checked={this.state.gradingmode}
          label="Gradingmode"
          onChange={this.handleSwitchGrading}
        />
      );
    }
    return null;
    // if the user has permissions it is also a source notebook

  }
}
