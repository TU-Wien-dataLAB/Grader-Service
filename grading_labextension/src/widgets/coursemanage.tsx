import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { CourseManageComponent } from '../components/coursemanage/coursemanage.component';

export class CourseManageView extends ReactWidget {
  /**
   * Construct a new grading widget
   */
  constructor(options: CourseManageView.IOptions = {}) {
    super();
    this.id = options.id;
    this.addClass('GradingWidget');
  }

  render() {
    const root = this.node;
    return <CourseManageComponent root={root} />;
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
