import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { GradingComponent } from '../components/grading/grading';


export class GradingView extends ReactWidget {

  public lectureID: number;
  public assignmentID: number;

  /**
   * Construct a new grading widget
   */
  constructor(options: GradingView.IOptions) {
    super();
    this.lectureID = options.lectureID;
    this.assignmentID = options.assignmentID;
    this.addClass('GradingWidget');
  }

  render() {
    return <GradingComponent lectureID={this.lectureID} assignmentID={this.assignmentID} title={this.title} />

  }

}

export namespace GradingView {
  /**
   * An options object for initializing a grading view widget.
   */
  export interface IOptions {
    lectureID: number;
    assignmentID: number;
  }
}