import * as React from 'react';
import { Assignment } from '../model/assignment';

export interface AssignmentProps {
  index: number;
  assignment: Assignment;
}

export class AssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public index: number;

  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
  }

  public render() {
    return <li key={this.index}>
      <div>
        <p>{this.assignment.name}</p>
        {this.assignment.exercises.map((ex, i) => <div>Exercise: {ex.name}</div>)}
        {this.assignment.files.map((file, i) => <div>File: {file.name}</div>)}
      </div>
    </li>
  }
}
