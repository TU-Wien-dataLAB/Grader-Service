import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { LectureListComponent } from '../components/assignment/lecture-list';

export class AssignmentList extends ReactWidget {
  /**
   * Construct a new assignment list widget
   */
  constructor(options: AssignmentList.IOptions = {}) {
    super();
    this.id = options.id;
    this.addClass('GradingWidget');
  }

  render(): JSX.Element {
    const root = this.node;
    return <LectureListComponent root={root} />;
  }
}

export namespace AssignmentList {
  /**
   * An options object for initializing a assignment list view widget.
   */
  export interface IOptions {
    /**
     * The widget/DOM id of the assignment list view.
     */
    id?: string;
  }
}
