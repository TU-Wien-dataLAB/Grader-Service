import { Cell } from '@jupyterlab/cells';
import { Panel } from '@lumino/widgets';
import { CellModel, NbgraderData, ToolData } from '../model';
import { GradeBook } from '../../../services/gradebook';

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
  private gradebook: GradeBook;
  private notebookName: string;

  constructor(cell: Cell, gradebook : GradeBook, notebookName: string) {
    super();
    this._cell = cell;
    const metadata = this.cell.model.metadata
    this.nbgraderData = CellModel.getNbgraderData(metadata);
    this.toolData = CellModel.newToolData(
      this.nbgraderData,
      this.cell.model.type
    );
    this.notebookName = notebookName;
    this.gradebook = gradebook;
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
    if (this.toolData.type !== "readonly" && this.toolData.type !== "") {
      const bodyElement = document.createElement('div');
      const commentElement = this.newCommentElement();
      const pointsElement = this.newPointsElement();
      const extraCreditElement = this.newExtraCreditElement();
      const elements = [];

      if (this.toolData.type === "manual" || this.toolData.type === "task") {
        elements[0] = commentElement;
        elements[1] = pointsElement;
        elements[2] = extraCreditElement;
      } else  if(this.toolData.type === "tests") {
        elements[0] = pointsElement;
        elements[1] = extraCreditElement;
      } else {
        elements[0] = commentElement;
      }
      const fragment = document.createDocumentFragment();
      for (const element of elements) {
        fragment.appendChild(element);
      }
      bodyElement.appendChild(fragment);
      this.node.appendChild(bodyElement);
    }
  }

  private newCommentElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_COMMENT;
    const label = document.createElement('label');
    label.textContent = 'Comment: ';
    const comment = document.createElement('input');
    try {
      comment.value = this.gradebook.getComment(this.notebookName, this.toolData.id);
    } catch {
      comment.value = "";
    }
    comment.onchange = () => {this.gradebook.setComment(this.notebookName,this.toolData.id,comment.value)
                                console.log(this.gradebook.properties)}
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
    try {
      input.value = String(this.gradebook.getGradeScore(this.notebookName, this.toolData.id));
    } catch {
      input.value = "0";
    }
    input.max = String(this.toolData.points)
    input.onchange = () => {this.gradebook.setManualScore(this.notebookName,this.toolData.id,+input.value)
      console.log(this.gradebook.properties)}
    label.appendChild(input);
    element.appendChild(label);
    return element;
  }

  private newExtraCreditElement(): HTMLDivElement {
    const element = document.createElement('div');
    element.className = CSS_CELL_POINTS;
    const label = document.createElement('label');
    label.textContent = 'Extra Credit: ';
    const input = document.createElement('input');
    input.type = 'number';
    input.min = '0';
    try {
      input.value = String(this.gradebook.getExtraCredit(this.notebookName, this.toolData.id));
    } catch {
      input.value = "0";
    }
    input.onchange = () => {this.gradebook.setExtraCredit(this.notebookName,this.toolData.id,+input.value)}
    label.appendChild(input);
    element.appendChild(label);
    return element;
  }

}
