import * as React from 'react';

import { Collapse } from '@jupyterlab/ui-components'

export interface AssignmentsProps {
  title: string;
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
    return <div className="AssignmentsComponent">
      <div onClick={this.toggleOpen} className="collapse-header">{this.title}</div>
      <Collapse isOpen={this.state.isOpen} className="collapse-body">
        <div>
          Dummy text.
        </div>
      </Collapse>
    </div>;
  }

}