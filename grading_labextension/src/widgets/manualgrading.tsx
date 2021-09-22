import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { ManualGradingComponent } from '../manual-grading/grade-view';


export class ManualGradingView extends ReactWidget {

  public lectureID: number;
  public assignmentID: number;
  public subID: number;

  /**
   * Construct a new grading widget
   */
  constructor(options: ManualGradingView.IOptions) {
    super();
    this.lectureID = options.lectureID;
    this.assignmentID = options.assignmentID;
    this.subID = options.subID;
    this.addClass('ManualGradingWidget');
  }

  render() {
    return <ManualGradingComponent lectureID={this.lectureID} assignmentID={this.assignmentID} title={this.title} subID={this.subID}/>

  }

}

export namespace ManualGradingView {
  /**
   * An options object for initializing a grading view widget.
   */
  export interface IOptions {
    lectureID: number;
    assignmentID: number;
    subID: number;
  }
}