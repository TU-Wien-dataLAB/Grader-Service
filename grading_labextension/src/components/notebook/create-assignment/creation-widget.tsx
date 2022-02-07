import { ReactWidget } from '@jupyterlab/apputils';
import { Alert, AlertTitle, Box, Grid, MenuItem, Select, TextField } from '@mui/material';
import * as React from 'react';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { IObservableJSON, IObservableMap } from '@jupyterlab/observables';
import { ReadonlyPartialJSONValue } from '@lumino/coreutils';

import { ReactElement, JSXElementConstructor } from 'react';
import { CellModel, CellType, NbgraderData, ToolData } from '../model';
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