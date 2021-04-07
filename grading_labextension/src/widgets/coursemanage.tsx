import * as React from 'react';
import {ReactWidget} from '@jupyterlab/apputils'
import { CourseManageComponent } from '../components/coursemanage.component';

export class CourseManageView extends ReactWidget {
  /**
   * Construct a new grading widget
   */
     constructor(options: CourseManageView.IOptions = {}) {
       super();
      this.id = options.id
      this.addClass('GradingWidget');
     }
     
     render() {
       return <CourseManageComponent />
     }

}

export namespace CourseManageView {
  /**
   * An options object for initializing a grading view widget.
   */
  export interface IOptions {
    /**
     * The widget/DOM id of the grading view.
     */
    id?: string;
  }
}