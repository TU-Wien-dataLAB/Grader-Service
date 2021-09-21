/* eslint-disable @typescript-eslint/explicit-module-boundary-types */

import { Switch } from '@blueprintjs/core';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { GradeCellWidget } from './grade-cell-widget';
import { UserPermissions, Scope } from '../services/permission.service';

export class ManualGradeSwitch extends ReactWidget {
  public ref: React.RefObject<ManualGradeSwitchComponent>;
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
      <ManualGradeSwitchComponent
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

export class ManualGradeSwitchComponent extends React.Component<ICreationmodeSwitchProps> {
  public state = {
    creationmode: false
  };
  public notebook: Notebook;
  public notebookpanel: NotebookPanel;
  public onChange: any;
  public isSourceNotebook: boolean;
  public hasCreationModePermissions: boolean;

  public constructor(props: ICreationmodeSwitchProps) {
    super(props);
    this.state.creationmode = props.creationmode || false;
    this.notebook = props.notebook;
    this.notebookpanel = props.notebookpanel;
    const notebookPaths: string[] = this.notebookpanel.context.contentsModel.path.split("/")
    console.log("Notebook path: " + this.notebookpanel.context.contentsModel.path)
    this.isSourceNotebook = notebookPaths[0] === "source"
    this.hasCreationModePermissions = false;
    if (this.isSourceNotebook) {
      const lectureCode = notebookPaths[1]
      if (UserPermissions.getPermissions().hasOwnProperty(lectureCode)) {
        this.hasCreationModePermissions = UserPermissions.getPermissions()[lectureCode] !== Scope.student;
      }
    }

    console.log("Source notebook: " + this.isSourceNotebook);
    console.log("Creation mode permissions: " + this.hasCreationModePermissions);
    this.onChange = this.props.onChange;
    this.handleSwitch = this.handleSwitch.bind(this);
  }

  public handleSwitch = () => {
    this.setState({ creationmode: !this.state.creationmode }, () => {
      this.onChange(this.state.creationmode);
      this.notebook.widgets.map((c: Cell) => {
        const currentLayout = c.layout as PanelLayout;
        if (this.state.creationmode) {
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
  };

  public render() {
    if (!this.hasCreationModePermissions) {
      return null;
    }

    // if the user has permissions it is also a source notebook
    return (
      <Switch
        checked={this.state.creationmode}
        label="Creationmode"
        onChange={this.handleSwitch}
      />
    );
  }
}