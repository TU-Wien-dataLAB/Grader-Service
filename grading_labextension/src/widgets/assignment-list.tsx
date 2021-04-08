import { ReactWidget } from '@jupyterlab/apputils';
import * as React from 'react';
import { CoursesComponent } from '../components/assignments/courses.component';


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
       return <CoursesComponent />
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