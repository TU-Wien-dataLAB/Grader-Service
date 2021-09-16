import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Spinner } from '@blueprintjs/core';

export class SpinnerWidget extends ReactWidget {

    public spinner: Spinner = new Spinner({ value: 0.0 })
    public fn: (spinner: Spinner) => void;

    public constructor(fn: (spinner: Spinner) => void) {
        super()
        this.fn = fn
    }

    protected render(): React.ReactElement<any, string | React.JSXElementConstructor<any>>[] | React.ReactElement<any, string | React.JSXElementConstructor<any>> {
        return
    }

}

export interface ISpinnerProps {
    fn: (spinner: Spinner) => void;
}

export class SpinnerComponent extends React.Component<ISpinnerProps> {

    public fn: (spinner: Spinner) => void;
    public state = {
        value: 0.0
    };

    public constructor(props: ISpinnerProps) {
        super(props);
        this.fn = props.fn;
    }
}