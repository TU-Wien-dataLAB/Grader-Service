/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Switch } from '@blueprintjs/core';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { Cell } from '@jupyterlab/cells';
import { PanelLayout } from '@lumino/widgets';
import { CellWidget } from './cellwidget';
import { CellPlayButton } from './widget';

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

export interface ICreationmodeSwitchProbs {
  creationmode: boolean;
  notebookpanel: NotebookPanel;
  notebook: Notebook;
  onChange: any;
}

export class CreationmodeSwitchComponent extends React.Component<ICreationmodeSwitchProbs> {
  public state = {
    creationmode: false
  };
  public notebook: Notebook;
  public notebookpanel: NotebookPanel;
  public onChange: any;

  public constructor(props: ICreationmodeSwitchProbs) {
    super(props);
    this.state.creationmode = props.creationmode || false;
    this.notebook = props.notebook;
    this.notebookpanel = props.notebookpanel;
    this.onChange = this.props.onChange;
    this.handleSwitch = this.handleSwitch.bind(this);
  }

  public handleSwitch = () => {
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
      /*new button add
      const cell: Cell = this.notebook.activeCell;
      const newButton: CellPlayButton = new CellPlayButton(
        cell,
        this.notebookpanel.sessionContext,
        this.state.creationmode
      );
      (cell.layout as PanelLayout).insertWidget(2, newButton);*/
    });
  };

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
