/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import { Switch } from '@blueprintjs/core';
import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';

export class CreationmodeSwitch extends ReactWidget {
  protected render() {
    return <CreationmodeSwitchComponent creationmode={false} />;
  }
}

export interface ICreationmodeSwitchProbs {
  creationmode: boolean;
}

export class CreationmodeSwitchComponent extends React.Component<ICreationmodeSwitchProbs> {
  public state = {
    creationmode: false
  };

  public constructor(props: ICreationmodeSwitchProbs) {
    super(props);
    this.state.creationmode = props.creationmode || false;
    this.handleSwitch = this.handleSwitch.bind(this);
  }

  public handleSwitch(): void {
    this.setState({ creationmode: !this.state.creationmode });
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
