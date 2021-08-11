/* eslint-disable no-var */
/* eslint-disable eqeqeq */
import { Styling } from '@jupyterlab/apputils';

import { Cell, ICellModel } from '@jupyterlab/cells';

import { IChangedArgs } from '@jupyterlab/coreutils';

import { IObservableJSON, IObservableMap } from '@jupyterlab/observables';

import { ReadonlyPartialJSONValue } from '@lumino/coreutils';

import { ISignal, Signal } from '@lumino/signaling';

import { Panel } from '@lumino/widgets';

import { CellModel, CellType, ToolData } from './model';

const CSS_CELL_HEADER = 'cellHeader';
const CSS_CELL_ID = 'cellId';
const CSS_CELL_POINTS = 'cellPoints';
const CSS_CELL_TYPE = 'cellType';
const CSS_CELL_WIDGET = 'cellWidget';
const CSS_LOCK_BUTTON = 'nbgrader-LockButton';
const CSS_MOD_ACTIVE = 'nbgrader-mod-active';
const CSS_MOD_HIGHLIGHT = 'nbgrader-mod-highlight';
const CSS_MOD_LOCKED = 'nbgrader-mod-locked';
const CSS_MOD_UNEDITABLE = 'nbgrader-mod-uneditable';
/**
 * Shows a cell's assignment data.
 */
export class CellWidget extends Panel {
  private _cell: Cell;
  private _click = new Signal<this, void>(this);
  private metadataChangedHandler: (
    metadata: IObservableJSON,
    changedArgs: IObservableMap.IChangedArgs<ReadonlyPartialJSONValue>
  ) => void;
  private onclick: (this: HTMLElement, ev: MouseEvent) => any;
  private lock: HTMLAnchorElement;
  private gradeId: HTMLDivElement;
  private points: HTMLDivElement;
  private taskInput: HTMLSelectElement;
  private gradeIdInput: HTMLInputElement;
  private pointsInput: HTMLInputElement;

  constructor(cell: Cell) {
    super();
    this._cell = cell;
    this.addMetadataListener(cell);
    this.initLayout();
    this.initClickListener();
    this.initInputListeners();
    this.initMetadata(cell);
    this.addClass(CSS_CELL_WIDGET);
  }

  private async addMetadataListener(cell: Cell) {
    await cell.ready;
    this.metadataChangedHandler = this.getMetadataChangedHandler();
    cell.model.metadata.changed.connect(this.metadataChangedHandler);
  }

  /**
   * The notebook cell associated with this widget.
   */
  get cell(): Cell {
    return this._cell;
  }

  private cleanNbgraderData(cell: Cell): void {
    CellModel.cleanNbgraderData(cell.model.metadata, cell.model.type);
  }

  /**
   * A signal for when this widget receives a click event.
   */
  get click(): ISignal<this, void> {
    return this._click;
  }

  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    if (this.metadataChangedHandler != null) {
      this.cell?.model?.metadata?.changed?.disconnect(
        this.metadataChangedHandler
      );
    }
    if (this.onclick != null) {
      this.node?.removeEventListener('click', this.onclick);
    }
    if (this.taskInput != null) {
      this.taskInput.onchange = null;
    }
    if (this.gradeIdInput != null) {
      this.gradeIdInput.onchange = null;
    }
    if (this.pointsInput != null) {
      this.pointsInput.onchange = null;
    }
    this._cell = null;
    this._click = null;
    this.metadataChangedHandler = null;
    this.onclick = null;
    this.lock = null;
    this.gradeId = null;
    this.points = null;
    this.taskInput = null;
    this.gradeIdInput = null;
    this.pointsInput = null;
    super.dispose();
  }

  private getCellStateChangedListener(
    srcPrompt: HTMLElement,
    destPrompt: HTMLElement
  ): (model: ICellModel, changedArgs: IChangedArgs<any, any, string>) => void {
    return (model: ICellModel, changedArgs: IChangedArgs<any, any, string>) => {
      if (changedArgs.name == 'executionCount') {
        destPrompt.innerText = srcPrompt.innerText;
      }
    };
  }

  private getMetadataChangedHandler(): (
    metadata: IObservableJSON,
    changedArgs: IObservableMap.IChangedArgs<ReadonlyPartialJSONValue>
  ) => void {
    return (
      metadata: IObservableJSON,
      changedArgs: IObservableMap.IChangedArgs<ReadonlyPartialJSONValue>
    ) => {
      const nbgraderData = CellModel.getNbgraderData(metadata);
      const toolData = CellModel.newToolData(
        nbgraderData,
        this.cell.model.type
      );
      this.updateValues(toolData);
    };
  }

  private getOnInputChanged(): () => void {
    return () => {
      const toolData = new ToolData();
      toolData.type = this.taskInput.value as CellType;
      if (!this.gradeId.classList.contains(CSS_MOD_UNEDITABLE)) {
        toolData.id = this.gradeIdInput.value;
      } else {
        const nbgraderData = CellModel.getNbgraderData(
          this.cell.model.metadata
        );
        if (nbgraderData?.grade_id == null) {
          toolData.id = 'cell-' + this.randomString(16);
        } else {
          toolData.id = nbgraderData.grade_id;
        }
        this.gradeIdInput.value = toolData.id;
      }
      if (!this.points.classList.contains(CSS_MOD_UNEDITABLE)) {
        toolData.points = this.pointsInput.valueAsNumber;
      }
      const data = CellModel.newNbgraderData(toolData);
      CellModel.setNbgraderData(data, this.cell.model.metadata);
    };
  }

  private getOnTaskInputChanged(): () => void {
    const onInputChanged = this.getOnInputChanged();
    return () => {
      onInputChanged();
      this.updateDisplayClass();
    };
  }

  private initClickListener(): void {
    this.onclick = () => {
      this._click.emit();
    };
    this.node.addEventListener('click', this.onclick);
  }

  private initInputListeners(): void {
    this.taskInput.onchange = this.getOnTaskInputChanged();
    this.gradeIdInput.onchange = this.getOnInputChanged();
    this.pointsInput.onchange = this.getOnInputChanged();
  }

  private initLayout(): void {
    const bodyElement = document.createElement('div');
    const headerElement = this.newHeaderElement();
    const taskElement = this.newTaskElement();
    const idElement = this.newIdElement();
    const pointsElement = this.newPointsElement();
    const elements = [taskElement, idElement, pointsElement];
    const fragment = document.createDocumentFragment();
    for (const element of elements) {
      fragment.appendChild(element);
    }
    bodyElement.appendChild(fragment);
    this.node.appendChild(bodyElement);
    this.lock = headerElement.getElementsByTagName('a')[0];
    this.gradeId = idElement;
    this.points = pointsElement;
    this.taskInput = taskElement.getElementsByTagName('select')[0];
    this.gradeIdInput = idElement.getElementsByTagName('input')[0];
    this.pointsInput = pointsElement.getElementsByTagName('input')[0];
  }

  private async initMetadata(cell: Cell) {
    await cell.ready;
    if (cell.model == null) {
      return;
    }
    this.cleanNbgraderData(cell);
    const nbgraderData = CellModel.getNbgraderData(cell.model.metadata);
    const toolData = CellModel.newToolData(nbgraderData, this.cell.model.type);
    CellModel.clearCellType(cell.model.metadata);
    this.updateDisplayClass();
    this.updateValues(toolData);
  }

  private newHeaderElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_HEADER;
    const promptNode = this.cell.promptNode.cloneNode(true) as HTMLElement;
    element.appendChild(promptNode);
    this.cell.model.stateChanged.connect(
      this.getCellStateChangedListener(this.cell.promptNode, promptNode)
    );
    const lockElement = document.createElement('a');
    lockElement.className = CSS_LOCK_BUTTON;
    const listElement = document.createElement('li');
    listElement.className = 'fa fa-lock';
    listElement.title = 'Student changes will be overwritten';
    lockElement.appendChild(listElement);
    element.appendChild(lockElement);
    return element;
  }

  private newIdElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_ID;
    const label = document.createElement('label');
    label.textContent = 'ID: ';
    const input = document.createElement('input');
    input.type = 'text';
    label.appendChild(input);
    element.appendChild(label);
    return element;
  }

  private newPointsElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_POINTS;
    const label = document.createElement('label');
    label.textContent = 'Points: ';
    const input = document.createElement('input');
    input.type = 'number';
    input.min = '0';
    label.appendChild(input);
    element.appendChild(label);
    return element;
  }

  private newTaskElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_TYPE;
    const label = document.createElement('label');
    label.textContent = 'Type: ';
    const select = document.createElement('select');
    const options = new Map<string, string>([
      ['', '-'],
      ['manual', 'Manually graded answer'],
      ['task', 'Manually graded task'],
      ['solution', 'Autograded answer'],
      ['tests', 'Autograded tests'],
      ['readonly', 'Read-only']
    ]);
    if (this.cell.model.type !== 'code') {
      options.delete('solution');
      options.delete('tests');
    }
    const fragment = document.createDocumentFragment();
    for (const optionEntry of options.entries()) {
      const option = document.createElement('option');
      option.value = optionEntry[0];
      option.innerHTML = optionEntry[1];
      fragment.appendChild(option);
    }
    select.appendChild(fragment);
    const selectWrap = Styling.wrapSelect(select);
    label.appendChild(selectWrap);
    element.appendChild(label);
    return element;
  }

  private randomString(length: number): string {
    var result = '';
    var chars = 'abcdef0123456789';
    var i;
    for (i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  }

  /**
   * Sets this cell as active/focused.
   */
  setActive(active: boolean): void {
    if (active) {
      this.addClass(CSS_MOD_ACTIVE);
    } else {
      this.removeClass(CSS_MOD_ACTIVE);
    }
  }

  private setGradeId(value: string): void {
    this.gradeIdInput.value = value;
  }

  private setElementEditable(element: HTMLElement, visible: boolean): void {
    if (visible) {
      element.classList.remove(CSS_MOD_UNEDITABLE);
    } else {
      element.classList.add(CSS_MOD_UNEDITABLE);
    }
  }

  private setGradeIdEditable(visible: boolean): void {
    this.setElementEditable(this.gradeId, visible);
  }

  private setPoints(value: number): void {
    this.pointsInput.value = value.toString();
  }

  private setPointsEditable(visible: boolean): void {
    this.setElementEditable(this.points, visible);
  }

  private setTask(value: string): void {
    this.taskInput.value = value;
  }

  private updateDisplayClass(): void {
    const data = CellModel.getNbgraderData(this.cell.model.metadata);
    if (CellModel.isRelevantToNbgrader(data)) {
      this.addClass(CSS_MOD_HIGHLIGHT);
    } else {
      this.removeClass(CSS_MOD_HIGHLIGHT);
    }
  }

  private updateValues(data: ToolData): void {
    this.setTask(data.type);
    if (data.id == null) {
      this.setGradeIdEditable(false);
      this.setGradeId('');
    } else {
      this.setGradeId(data.id);
      this.setGradeIdEditable(true);
    }
    if (data.points == null) {
      this.setPointsEditable(false);
      this.setPoints(0);
    } else {
      this.setPoints(data.points);
      this.setPointsEditable(true);
    }
    if (data.locked) {
      this.lock.classList.add(CSS_MOD_LOCKED);
    } else {
      this.lock.classList.remove(CSS_MOD_LOCKED);
    }
  }
}
