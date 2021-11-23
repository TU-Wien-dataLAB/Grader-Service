import { Button, Switch } from '@blueprintjs/core';
import { Cell } from '@jupyterlab/cells';
import { Notebook, NotebookPanel } from '@jupyterlab/notebook';
import { PanelLayout } from "@lumino/widgets";
import React from 'react';
import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';
import { GradeBook } from '../../../services/gradebook';
import { ImodeSwitchProps } from "../slider";
import { CellWidget } from './cellwidget';
import { CellPlayButton } from './widget';

export class CreationModeSwitch extends React.Component<ImodeSwitchProps> {
    public state = {
        mode: false,
      };
      private notebook: Notebook;
      private notebookpanel: NotebookPanel;
      private notebookPaths
      private lecture: Lecture;
      private assignment: Assignment;
      private gradeBook: GradeBook;
      private onChange: any;
    
      public constructor(props: ImodeSwitchProps) {
        super(props);
        this.state.mode = props.mode || false;
        this.notebook = props.notebook;
        this.notebookpanel = props.notebookpanel;
        this.notebookPaths = this.notebookpanel.context.contentsModel.path.split("/");
        this.onChange = this.props.onChange;
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