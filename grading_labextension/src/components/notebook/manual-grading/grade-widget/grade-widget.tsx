import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import { Cell } from '@jupyterlab/cells';

import { ReactElement, JSXElementConstructor } from 'react';
import { GradeBook } from '../../../../services/gradebook';
import { GradeComponent } from './grade-component';
import { CellModel, NbgraderData, ToolData } from '../../model';

export class GradeWidget extends ReactWidget {
    public cell: Cell;
    public gradebook: GradeBook;
    public nbname: string;
    public nbgraderData: NbgraderData;
    public toolData: ToolData;

    constructor(cell: Cell, gradebook: GradeBook, nbname: string) {
        super();
        this.cell = cell;
        this.gradebook = gradebook;
        this.nbname = nbname;
        this.nbgraderData = CellModel.getNbgraderData(this.cell.model.metadata);
        this.toolData = CellModel.newToolData(this.nbgraderData,this.cell.model.type);
        }


    protected render(): ReactElement<any, string | JSXElementConstructor<any>>[] | ReactElement<any, string | JSXElementConstructor<any>> {
        if(this.toolData.type !== "" && this.toolData.type !== "readonly" ) {
            return (<GradeComponent nbgraderData={this.nbgraderData} toolData={this.toolData} gradebook={this.gradebook} nbname={this.nbname}/>);
        } else {
            return null;
        }
    }
}