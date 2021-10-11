import { ReactWidget } from '@jupyterlab/apputils';
import React from 'react';
import { FeedbackComponent } from '../components/assignments/feedback.component';

export class FeedbackView extends ReactWidget {

    public lectureID: number;
    public assignmentID: number;
    public subID: number;
    public username: string;
  
    /**
     * Construct a new grading widget
     */
    constructor(options: FeedbackView.IOptions) {
      super();
      this.lectureID = options.lectureID;
      this.assignmentID = options.assignmentID;
      this.subID = options.subID;
      this.username = options.username;
      this.addClass('ManualGradingWidget');
    }
  
    render() {
      return <FeedbackComponent lectureID={this.lectureID} assignmentID={this.assignmentID} title={this.title} subID={this.subID} username={this.username} />
    }
  
  }
  
  export namespace FeedbackView {
    /**
     * An options object for initializing a feedback view widget.
     */
    export interface IOptions {
      lectureID: number;
      assignmentID: number;
      subID: number;
      username: string;
    }
  }