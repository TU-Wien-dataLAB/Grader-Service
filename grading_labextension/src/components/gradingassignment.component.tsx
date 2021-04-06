import * as React from 'react';
import { Assignment } from '../model/assignment';
import { Button } from '@jupyterlab/ui-components';

export interface AssignmentProps {
  index: number;
  assignment: Assignment;
}

export class AssignmentGradingComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public index: number;

  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
  }

  public render() {
    return <li key={this.index}>
        <p>{this.assignment.name}</p>
        <Button icon='edit' minimal></Button>
        <Button icon='search' minimal></Button>
        <Button icon='cloud-upload' minimal></Button>
        <Button icon='cloud-download' minimal></Button>
        {this.assignment.exercises.map((ex, i) => <div>Exercise: {ex.name}</div>)}
        {this.assignment.files.map((file, i) => <div>File: {file.name}</div>)}
    </li>
  }
}
