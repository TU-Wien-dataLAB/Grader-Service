import * as React from 'react';
import { Assignment } from '../model/assignment';

import { Icon, Collapse } from "@blueprintjs/core";
import { IconNames } from "@blueprintjs/icons";

import { GlobalObjects } from '../index';
import { showErrorMessage } from '@jupyterlab/apputils'

// import { DockLayout, Widget } from '@lumino/widgets';

export interface AssignmentProps {
  index: number;
  lectureName: string,
  assignment: Assignment;
}

export class AssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lectureName: string;
  public index: number;
  public state = {
    isOpen: true,
  };

  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
    this.lectureName = props.lectureName;
  }

  private toggleOpen = () => {
    console.log("toggle assignment header")
    this.setState({ isOpen: !this.state.isOpen });
  }

  private openFile(path: string) {
    console.log("Opening file: " + path)
    GlobalObjects.commands.execute('docmanager:open', {
      path: path,
      options: {
        mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
      }
    }).catch(error => {
      showErrorMessage("Error Opening File", error)
    })
  }

  public render() {
    return <li key={this.index}>
      <div className="assignment">
        <div onClick={this.toggleOpen} className="assignment-header">
          <Icon icon={IconNames.CHEVRON_RIGHT} iconSize={12}
            className={`collapse-icon-small ${this.state.isOpen ? "collapse-icon-small-open" : ""}`}></Icon>
          <Icon icon={IconNames.INBOX} iconSize={12} className="flavor-icon"></Icon>
          {this.assignment.name}
        </div>
        <Collapse isOpen={this.state.isOpen}>
          <div className="assignment-content">
            {this.assignment.exercises.map((ex, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${ex.name}`)}>
                <Icon icon={IconNames.EDIT} iconSize={12} className="flavor-icon"></Icon>
                {ex.name}
              </div>
            )}

            {this.assignment.files.map((file, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${file.name}`)}>
                <Icon icon={IconNames.DOCUMENT} iconSize={12} className="flavor-icon"></Icon>
                {file.name}
              </div>
            )}
          </div>
        </Collapse>
      </div>
    </li>
  }
}
