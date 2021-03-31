import { ReactWidget } from '@jupyterlab/apputils';
import { AssignmentsComponent } from '../components/assignment.component'
import * as React from 'react';


export class AssignmentList extends ReactWidget {
  /*
   * Construct a new grading widget
   */
     constructor(options: AssignmentList.IOptions = {}) {
      super();
      this.id = options.id

      this.addClass('AssignmentListWidget');
     }

     render() {
       return <AssignmentsComponent title="Test" open={true} />
     }
}

export namespace AssignmentList {
  /**
   * An options object for initializing an assignment list widget.
   */
  export interface IOptions {
    /**
     * The widget/DOM id of the assignment list.
     */
    id?: string;
  }
}