import { Cell } from '@jupyterlab/cells';
import { Panel } from '@lumino/widgets';
import { CellModel, NbgraderData, ToolData } from '../create-assignment/model';

const CSS_CELL_HEADER = 'cellHeader';
const CSS_CELL_COMMENT = 'cellComment';
const CSS_CELL_POINTS = 'cellPoints';
const CSS_CELL_WIDGET = 'cellWidget';
/**
 * Shows a cell's assignment data.
 */
export class GradeCommentCellWidget extends Panel {
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
    if (this.toolData.type !== "readonly") {
      const bodyElement = document.createElement('div');
      const headerElement = this.newHeaderElement();
      const commentElement = this.newCommentElement();
      const elements = [commentElement];

      if (this.toolData.type !== "solution") {
        const pointsElement = this.newPointsElement();
        elements[1] = pointsElement;
      }
      const fragment = document.createDocumentFragment();
      for (const element of elements) {
        fragment.appendChild(element);
      }
      bodyElement.appendChild(fragment);
      this.node.appendChild(bodyElement);
    }
  }

  private newHeaderElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_HEADER;
    return element;
  }

  private newCommentElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_COMMENT;
    const label = document.createElement('label');
    label.textContent = 'Comment: ';
    const comment = document.createElement('input');
    comment.type = 'text';
    element.appendChild(label)
    element.appendChild(comment);
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
    input.max = String(this.toolData.points)
    label.appendChild(input);
    element.appendChild(label);
    return element;
  }
}
