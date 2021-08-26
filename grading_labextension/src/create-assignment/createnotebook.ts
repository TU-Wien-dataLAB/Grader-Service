/* eslint-disable prettier/prettier */
import { Notebook } from '@jupyterlab/notebook';
import { Cell, ICellModel } from '@jupyterlab/cells';


export class CreateNotebook extends Notebook {
    protected onCellInserted(index : number, cell: Cell<ICellModel>) : void {
        super.onCellInserted(index,cell)
    }
}