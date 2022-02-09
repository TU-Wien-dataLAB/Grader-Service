import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import { Cell } from '@jupyterlab/cells';

import { ReactElement, JSXElementConstructor } from 'react';
import { GradeBook } from '../../../services/gradebook';
import { GradeComponent } from './grade-component';

export class GradeWidget extends ReactWidget {
    public cell: Cell;
    public gradebook: GradeBook;
    public nbname: string;

    constructor(cell: Cell, gradebook: GradeBook, nbname: string) {
        super();
        this.cell = cell;
        this.gradebook = gradebook;
        this.nbname = nbname
        }


    protected render(): ReactElement<any, string | JSXElementConstructor<any>>[] | ReactElement<any, string | JSXElementConstructor<any>> {
        return (<GradeComponent cell={this.cell} gradebook={this.gradebook} nbname={this.nbname}/>);
    }
}