import * as React from 'react';
import { DirListing } from '@jupyterlab/filebrowser/lib/listing';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { ExistingNodeRenderer } from '../components/assignments/assignment.component';
import moment from 'moment';
import { showErrorMessage } from '@jupyterlab/apputils';

import { GlobalObjects } from '../index';
import { Contents } from '@jupyterlab/services';
import { Title, Widget } from '@lumino/widgets';
import { Lecture } from '../model/lecture';
import { getLecture } from '../services/lectures.service';
import { Assignment } from '../model/assignment';
import { fetchAssignment } from '../services/assignments.service';
import { Submission } from '../model/submission';
import { getProperties } from '../services/submissions.service';
import { Button } from '@blueprintjs/core';

export interface ManualGradingProps {
  lectureID: number;
  assignmentID: number;
  subID: number;
  title: Title<Widget>;
}

export class ManualGradingComponent extends React.Component<ManualGradingProps> {

  public dirListingNode: HTMLElement;
  public dirListing: DirListing;
  private lectureID: number;
  private assignmentID: number;
  private subID: number;
  private title: Title<Widget>;
  private submissionProperties: object;

  constructor(props: ManualGradingProps) {
    super(props);
    this.lectureID = props.lectureID;
    this.assignmentID = props.assignmentID;
    this.title = props.title;
    this.subID = props.subID;
    this.submissionProperties = null;
  }

  public async componentDidMount() {
    this.submissionProperties = await getProperties(this.lectureID, this.assignmentID, this.subID).toPromise();
    console.log("submissionProperties")
    console.log(this.submissionProperties)
    const assignment: Assignment = await fetchAssignment(
      this.lectureID,
      this.assignmentID,
      false,
      true
    ).toPromise();

    const lecture: Lecture = await getLecture(this.lectureID).toPromise();

    this.title.label = `Manualgrade ${assignment.name}`;
    const renderer = new ExistingNodeRenderer(this.dirListingNode);
    const model = new FilterFileBrowserModel({
      auto: true,
      manager: GlobalObjects.docManager
    });

    const LISTING_CLASS = 'jp-FileBrowser-listing';
    this.dirListing = new DirListing({ model, renderer });
    this.dirListing.addClass(LISTING_CLASS);
    const manualPath = `manualgrade/${lecture.code}/${assignment.name}/${this.subID}`
    await model.cd(manualPath);
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
      .catch(error => {
        showErrorMessage('Error Opening File', error);
      });
  }

  public render() {
    return (
      <div>
        <h1>
          <p style={{ textAlign: 'center' }}>Manualgrade</p>
        </h1>
        <div
          className="assignment-dir-listing"
          ref={_element => (this.dirListingNode = _element)}
        >
        </div>
        <Button>Check Grading Status</Button>
      </div>
    )
  }

}