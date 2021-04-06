import * as React from 'react';
import {ReactWidget} from '@jupyterlab/apputils'
import { GradingComponent } from '../components/grading.component';

export class GradingView extends ReactWidget {
  /**
   * Construct a new grading widget
   */
     constructor(options: GradingView.IOptions = {}) {
       super();
      this.id = options.id
      this.addClass('GradingWidget');
     }
     
     render() {
       return <GradingComponent />
     }

}

export namespace GradingView {
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