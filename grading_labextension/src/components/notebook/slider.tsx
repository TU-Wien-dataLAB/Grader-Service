/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Button, Intent, Divider, Switch } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { SwitchModeFactory } from './switch-factory';

export class NotebookModeSwitch extends ReactWidget {
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
    const props : ImodeSwitchProps = {notebook: notebook, notebookpanel: notebookpanel, mode: mode, onChange: onChange};
    this.component = SwitchModeFactory.getSwitch(props);
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