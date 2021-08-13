/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Switch } from '@blueprintjs/core';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { CellWidget } from './cellwidget';

export class CreationmodeSwitch extends ReactWidget {
  public ref: React.RefObject<CreationmodeSwitchComponent>;
  component: JSX.Element;
  constructor(
    creationmode: boolean,
    notebookpanel: NotebookPanel,
    notebook: Notebook
  ) {
    super();
    this.component = (
      <CreationmodeSwitchComponent
        notebook={notebook}
        notebookpanel={notebookpanel}
        creationmode={creationmode}
      />
    );
  }

  protected render() {
    return this.component;
  }
}

export interface ICreationmodeSwitchProbs {
  creationmode: boolean;
  notebookpanel: NotebookPanel;
  notebook: Notebook;
}

export class CreationmodeSwitchComponent extends React.Component<ICreationmodeSwitchProbs> {
  public state = {
    creationmode: false
  };
  public notebook: Notebook;
  public notebookpanel: NotebookPanel;

  public constructor(props: ICreationmodeSwitchProbs) {
    super(props);
    this.state.creationmode = props.creationmode || false;
    this.notebook = props.notebook;
    this.notebookpanel = props.notebookpanel;
    this.handleSwitch = this.handleSwitch.bind(this);
  }

  public handleSwitch(): void {
    this.setState({ creationmode: !this.state.creationmode }, () => {
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
      });
    });
  }

  public render() {
    return (
      <Switch
        checked={this.state.creationmode}
        label="Creationmode"
        onChange={this.handleSwitch}
      />
    );
  }
}
