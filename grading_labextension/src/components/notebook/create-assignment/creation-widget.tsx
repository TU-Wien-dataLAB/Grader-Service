import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import { Cell } from '@jupyterlab/cells';

import { ReactElement, JSXElementConstructor } from 'react';
import { CreationComponent } from './creation-component';


export class CreationWidget extends ReactWidget {
    public cell: Cell;

    constructor(cell: Cell) {
        super();
        this.cell = cell;

        }


    protected render(): ReactElement<any, string | JSXElementConstructor<any>>[] | ReactElement<any, string | JSXElementConstructor<any>> {
        return (<CreationComponent cell={this.cell}/>);
    }
}