// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import { Cell } from '@jupyterlab/cells';

import { ReactElement, JSXElementConstructor } from 'react';
import { CreationComponent } from './creation-component';
import { ErrorComponent } from './error-component';


export class ErrorWidget extends ReactWidget {
    public cell: Cell;
    public err: string;

    constructor(cell: Cell, err: string) {
        super();
        this.cell = cell;
        this.err = err;

        }

    protected render(): ReactElement<any, string | JSXElementConstructor<any>>[] | ReactElement<any, string | JSXElementConstructor<any>> {
        return (<ErrorComponent err={this.err}/>);
    }
}