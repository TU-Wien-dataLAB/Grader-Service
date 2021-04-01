import * as React from 'react';

import { Collapse } from '@jupyterlab/ui-components'

export interface AssignmentsProps {
  lect_id: number; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class AssignmentsComponent extends React.Component<AssignmentsProps> {
  public title: string;
  public state = {
    isOpen: false,
  };

  constructor(props: AssignmentsProps) {
    super(props)
    this.title = props.title
    this.state.isOpen = props.open || false
  }

  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
  }

  public render() {
    let test_list = [0,1,2,3,4,5,6,7]
    return <div className="AssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">{this.title}</div>
      <Collapse isOpen={this.state.isOpen} className="collapse-body">
        <ul>
          {test_list.map((el, index) => <li key={index}>{"Assignment " + el}</li>)}
        </ul>
      </Collapse>
    </div>;
  }

}