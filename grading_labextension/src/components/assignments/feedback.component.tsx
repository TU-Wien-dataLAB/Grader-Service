import * as React from 'react';
import { DirListing } from '@jupyterlab/filebrowser/lib/listing';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { ExistingNodeRenderer } from '../../components/assignments/assignment.component';
import moment from 'moment';
import { showErrorMessage } from '@jupyterlab/apputils';

import { GlobalObjects } from '../../index';
import { Contents } from '@jupyterlab/services';
import { Title, Widget } from '@lumino/widgets';
import { Lecture } from '../../model/lecture';
import { getLecture } from '../../services/lectures.service';
import { Assignment } from '../../model/assignment';
import { fetchAssignment } from '../../services/assignments.service';
import { Submission } from '../../model/submission';
import { getProperties } from '../../services/submissions.service';
import { Button, Intent, Divider, Tag } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import { GradeBook } from '../../services/gradebook';

export interface FeedbackProps {
  lectureID: number;
  assignmentID: number;
  subID: number;
  title: Title<Widget>;
}

export class FeedbackComponent extends React.Component<FeedbackProps> {

  public dirListingNode: HTMLElement;
  public dirListing: DirListing;
  private lectureID: number;
  private assignmentID: number;
  private subID: number;
  private title: Title<Widget>;
  private gradeBook: GradeBook;
  public state = {
    lecture: {} as Lecture,
    assignment: {} as Assignment,
    points: 0.0,
    maxPoints: 0.0,
    extraCredit: 0.0,
    gradingInfo: new Map<string, boolean>(),
  }

  constructor(props: FeedbackProps) {
    super(props);
    this.lectureID = props.lectureID;
    this.assignmentID = props.assignmentID;
    this.title = props.title;
    this.subID = props.subID;
  }

  public async componentDidMount() {
    this.setState({
      assignment: await fetchAssignment(
        this.lectureID,
        this.assignmentID,
        false,
        true
      ).toPromise()
    });

    this.setState({ lecture: await getLecture(this.lectureID).toPromise() });
    const properties = await getProperties(this.lectureID, this.assignmentID, this.subID).toPromise();
    this.gradeBook = new GradeBook(properties);
    this.setState({
      points: this.gradeBook.getPoints(),
      maxPoints: this.gradeBook.getMaxPoints(),
      gradingInfo: this.gradeBook.getGradingInfo(),
      extraCredit: this.gradeBook.getExtraCredits()
    });

    this.title.label = `Feedback ID: ${this.subID}`;
    const renderer = new ExistingNodeRenderer(this.dirListingNode);
    const model = new FilterFileBrowserModel({
      auto: true,
      manager: GlobalObjects.docManager
    });

    const LISTING_CLASS = 'jp-FileBrowser-listing';
    this.dirListing = new DirListing({ model, renderer });
    this.dirListing.addClass(LISTING_CLASS);
    const feedbackPath = `feedback/${this.state.lecture.code}/${this.state.assignment.name}/${this.subID}`
    await model.cd(feedbackPath);
    this.dirListingNode.onclick = async ev => {
      const model = this.dirListing.modelForClick(ev);
      if (model == undefined) {
        this.dirListing.handleEvent(ev);
        return;
      }
      if (!this.dirListing.isSelected(model.name)) {
        await this.dirListing.selectItemByName(model.name);
      } else {
        this.dirListing.clearSelectedItems();
        this.dirListing.update();
      }
    };
    this.dirListingNode.ondblclick = ev => {
      const model = this.dirListing.modelForClick(ev);
      this.openFile(model.path);
    };
    this.dirListingNode.oncontextmenu = ev => {
      ev.preventDefault();
      ev.stopPropagation();
    };
  }

  private openFile(path: string) {
    console.log('Opening file: ' + path);
    GlobalObjects.commands
      .execute('docmanager:open', {
        path: path,
        options: {
          mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
        }
      })
      .catch((error: any) => {
        showErrorMessage('Error Opening File', error);
      });
  }

  private async reload() {
    const properties = await getProperties(this.lectureID, this.assignmentID, this.subID).toPromise();
    this.gradeBook = new GradeBook(properties);
    this.setState({
      points: this.gradeBook.getPoints(),
      maxPoints: this.gradeBook.getMaxPoints(),
      gradingInfo: this.gradeBook.getGradingInfo(),
      extraCredit: this.gradeBook.getExtraCredits()
    });
  }

  public render() {
    return (
      <div>
        <h1>
          <p style={{ textAlign: 'center' }}>Feedback</p>
        </h1>
        <div id="manual-grade-container">
          <div id="info-container">
            <h2>Information</h2>
            <ul className="manual-grading-list">
              <li>Lecture: <Tag minimal round>{this.state.lecture.name}</Tag></li><Divider />
              <li>Assignment: <Tag minimal round>{this.state.assignment.name}</Tag></li><Divider />
              <li>Type: <Tag minimal round>{this.state.assignment.type}</Tag></li><Divider />
              <li>Points: <Tag minimal round>{this.state.points}/{this.state.maxPoints}</Tag></li><Divider />
              <li>Extra Credit: <Tag minimal round>{this.state.extraCredit}</Tag></li><Divider />
            </ul>
          </div>
          <h2>Feedback</h2>
          <div
            className="assignment-dir-listing"
            ref={_element => (this.dirListingNode = _element)}
          >
          </div>
        </div>
      </div>
    )
  }

}