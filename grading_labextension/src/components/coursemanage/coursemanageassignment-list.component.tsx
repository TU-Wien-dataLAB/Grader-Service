import * as React from 'react';
import {
  createAssignment,
  getAllAssignments
} from '../../services/assignments.service';
import { Collapse } from '@jupyterlab/ui-components';
import { Assignment } from '../../model/assignment';
import { CourseManageAssignmentComponent } from './coursemanageassignment.component';
import { Button, Card, Elevation, Icon } from '@blueprintjs/core';
import {
  Dialog,
  showDialog,
  showErrorMessage
} from '@jupyterlab/apputils/lib/dialog';
import { Widget } from '@lumino/widgets';
import { Lecture } from '../../model/lecture';

const INPUT_DIALOG_CLASS = 'jp-Input-Dialog';
/**
 * Namespace for input dialogs
 */
export var InputDialog: any;
(function (InputDialog) {
  /**
   * Create and show a input dialog for a text.
   *
   * @param options - The dialog setup options.
   *
   * @returns A promise that resolves with whether the dialog was accepted
   */
  function getText(options: any) {
    return showDialog(
      Object.assign(Object.assign({}, options), {
        body: new InputTextDialog(options),
        buttons: [
          Dialog.cancelButton({ label: options.cancelLabel }),
          Dialog.okButton({ label: options.okLabel })
        ],
        focusNodeSelector: 'input'
      })
    );
  }
  InputDialog.getText = getText;

  function getDate(options: any) {
    return showDialog(
      Object.assign(Object.assign({}, options), {
        body: new InputDateDialog(options),
        buttons: [
          Dialog.cancelButton({ label: options.cancelLabel }),
          Dialog.okButton({ label: options.okLabel })
        ],
        focusNodeSelector: 'input'
      })
    );
  }
  InputDialog.getDate = getDate;
})(InputDialog || (InputDialog = {}));
/**
 * Base widget for input dialog body
 */
class InputDialogBase extends Widget {
  /**
   * InputDialog constructor
   *
   * @param label Input field label
   */
  constructor(label: string) {
    super();
    this.addClass(INPUT_DIALOG_CLASS);
    if (label !== undefined) {
      const labelElement = document.createElement('label');
      labelElement.textContent = label;
      // Initialize the node
      this.node.appendChild(labelElement);
    }
  }
}

class InputDateDialog extends InputDialogBase {
  private _input: any;
  /**
   * constructor
   *
   * @param options Constructor options
   */
  constructor(options: { label: any; text: any; placeholder: any }) {
    super(options.label);

    this._input = document.createElement('input');
    this._input.classList.add('jp-mod-styled');
    this._input.type = 'datetime-local';
    this._input.value = options.text ? options.text : '';
    if (options.placeholder) {
      this._input.placeholder = options.placeholder;
    }
    // Initialize the node
    this.node.appendChild(this._input);
  }
  /**
   * Get the text specified by the user
   */
  getValue() {
    return this._input.value;
  }
}

/**
 * Widget body for input text dialog
 */
class InputTextDialog extends InputDialogBase {
  private _input: any;
  /**
   * InputTextDialog constructor
   *
   * @param options Constructor options
   */
  constructor(options: { label: any; text: any; placeholder: any }) {
    super(options.label);
    this._input = document.createElement('input', {});
    this._input.classList.add('jp-mod-styled');
    this._input.type = 'text';
    this._input.value = options.text ? options.text : '';
    if (options.placeholder) {
      this._input.placeholder = options.placeholder;
    }
    // Initialize the node
    this.node.appendChild(this._input);
  }
  /**
   * Get the text specified by the user
   */
  getValue() {
    return this._input.value;
  }
}

export interface AssignmentListProps {
  lecture: Lecture; // assignment id
  title: string; // course title
  open?: boolean; // initial state of collapsable
}

export class CourseManageAssignmentsComponent extends React.Component<AssignmentListProps> {
  public lecture: Lecture;
  public title: string;
  public state = {
    isOpen: true,
    assignments: new Array<Assignment>()
  };

  constructor(props: AssignmentListProps) {
    super(props);
    this.title = props.title;
    this.lecture = props.lecture;
    this.state.isOpen = props.open || false;
    this.getAssignments = this.getAssignments.bind(this);
  }

  private async createAssignment(id: number) {
    try {
      let input = await InputDialog.getText({ title: 'Input assignment name' });
      //TODO: Implement own InputDialog to set Date correct
      if (input.button.accept) {
        let assignment = await createAssignment(id, {
          name: input.value,
          due_date: null,
          status: 'created'
        }).toPromise();

        console.log(assignment);

        this.setState(
          { assignments: [...this.state.assignments, assignment] },
          () => {
            console.log('New State:' + JSON.stringify(this.state.assignments));
          }
        );
      }
    } catch (e) {
      showErrorMessage('Error Creating Assignment', e);
    }
  }

  private toggleOpen = () => {
    this.setState({ isOpen: !this.state.isOpen });
  };

  public componentDidMount() {
    this.getAssignments();
  }

  private getAssignments() {
    getAllAssignments(this.lecture.id).subscribe(
      assignments => this.setState({assignments}),
      error => showErrorMessage('Error Loading Assignments', error));
  }

  public render() {
    return (
      <div className="assignment-list">
        <Card elevation={Elevation.TWO}>
          <div onClick={this.toggleOpen} className="collapse-header">
            <Icon icon="learning" className="flavor-icon"></Icon>
            <Icon
              icon="chevron-down"
              className={`collapse-icon ${
                this.state.isOpen ? 'collapse-icon-open' : ''
              }`}
            ></Icon>
            {this.title}
          </div>

          <Collapse
            isOpen={this.state.isOpen}
            className="collapse-body"
            keepChildrenMounted={true}
          >
            <ul>
              {this.state.assignments.map((el, index) => (
                <CourseManageAssignmentComponent
                  parentUpdate={this.getAssignments}
                  index={index}
                  lectureName={this.title}
                  lecture={this.lecture}
                  assignment={el}
                  assignments={this.state.assignments}
                />
              ))}
            </ul>
            <div className="assignment-create">
              <Button
                icon="add"
                outlined
                onClick={() => this.createAssignment(this.lecture.id)}
                className="assignment-button"
              >
                Create new Assignment
              </Button>
            </div>
          </Collapse>
        </Card>
      </div>
    );
  }
}
