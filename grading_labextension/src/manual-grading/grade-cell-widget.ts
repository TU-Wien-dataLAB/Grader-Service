import { Cell } from '@jupyterlab/cells';
import { Panel } from '@lumino/widgets';
import { CellModel, NbgraderData, ToolData } from '../create-assignment/model';

const CSS_CELL_HEADER = 'cellHeader';
const CSS_CELL_ID = 'cellId';
const CSS_CELL_POINTS = 'cellPoints';
const CSS_CELL_TYPE = 'cellType';
const CSS_CELL_WIDGET = 'cellWidget';
/**
 * Shows a cell's assignment data.
 */
export class GradeCellWidget extends Panel {
  private _cell: Cell;
  private nbgraderData: NbgraderData;
  private toolData: ToolData;

  constructor(cell: Cell) {
    super();
    this._cell = cell;
    const metadata = this.cell.model.metadata
    this.nbgraderData = CellModel.getNbgraderData(metadata);
    this.toolData = CellModel.newToolData(
        this.nbgraderData,
        this.cell.model.type
      );
    this.initLayout();
    this.addClass(CSS_CELL_WIDGET);

  }

  /**
   * The notebook cell associated with this widget.
   */
  get cell(): Cell {
    return this._cell;
  }

  private initLayout(): void {
    const bodyElement = document.createElement('div');
    const taskElement = this.newTaskElement();
    const idElement = this.newIdElement();
    const elements = [taskElement, idElement];
    if (this.toolData.type !== "solution" && this.toolData.type !== "readonly") {
      const pointsElement = this.newPointsElement();
      elements[2] = pointsElement;
    }
    const fragment = document.createDocumentFragment();
    for (const element of elements) {
      fragment.appendChild(element);
    }
    bodyElement.appendChild(fragment);
    this.node.appendChild(bodyElement);
  }

  private newIdElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_ID;
    const label = document.createElement('label');
    label.textContent = 'ID: ';
    const id = document.createElement('label');
    id.textContent = this.toolData.id

    label.appendChild(id);
    element.appendChild(label);
    return element;
  }

  private newPointsElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_POINTS;
    const label = document.createElement('label');
    label.textContent = 'Max Points: ';
    const points = document.createElement('label');
    points.textContent = String(this.toolData.points)
    label.appendChild(points);
    element.appendChild(label);
    return element;
  }

  private newTaskElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_TYPE;
    const label = document.createElement('label');
    label.textContent = 'Type: ';
    const task = document.createElement('label');
    const options = new Map<string, string>([
      ['', '-'],
      ['manual', 'Manually graded answer'],
      ['task', 'Manually graded task'],
      ['solution', 'Autograded answer'],
      ['tests', 'Autograded tests'],
      ['readonly', 'Read-only']
    ]);
    task.textContent = options.get(this.toolData.type)
    element.appendChild(label);
    element.appendChild(task);
    return element;
  }

}
