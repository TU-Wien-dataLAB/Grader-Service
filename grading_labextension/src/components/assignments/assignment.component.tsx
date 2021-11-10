import * as React from 'react';
import { Assignment } from '../../model/assignment';

import {
  Icon,
  Collapse,
  Button,
  Intent,
  Tag,
  Divider
} from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';
import { GlobalObjects } from '../../index';
import { showErrorMessage, showDialog, Dialog } from '@jupyterlab/apputils';
import { InputDialog } from '@jupyterlab/apputils/lib/inputdialog';
import { Submission } from '../../model/submission';
import {
  getSubmissions,
  submitAssignment,
  pullFeedback
} from '../../services/submissions.service';
import { pullAssignment } from '../../services/assignments.service';
import { Lecture } from '../../model/lecture';
import { DirListing } from '@jupyterlab/filebrowser/lib/listing';
import { FilterFileBrowserModel } from '@jupyterlab/filebrowser/lib/model';
import { DeadlineComponent } from './deadline.component';
import { utcToLocalFormat } from '../../services/datetime.service';

export interface AssignmentProps {
  index: number;
  lecture: Lecture;
  assignment: Assignment;
}

export class ExistingNodeRenderer extends DirListing.Renderer {
  private node: HTMLElement;

  constructor(node: HTMLElement) {
    super();
    this.node = node;
  }

  createNode(): HTMLElement {
    const CONTENT_CLASS = 'jp-DirListing-content';
    const HEADER_CLASS = 'jp-DirListing-header';

    const header = document.createElement('div');
    const content = document.createElement('ul');
    content.className = CONTENT_CLASS;
    header.className = HEADER_CLASS;

    this.node.innerHTML = '';
    this.node.appendChild(header);
    this.node.appendChild(content);
    this.node.tabIndex = 0;

    return this.node;
  }
}

export class AssignmentComponent extends React.Component<AssignmentProps> {
  public lecture: Lecture;
  public index: number;
  public iconSize: number = 14;
  public state = {
    filesOpen: false,
    submissionsOpen: false,
    submissions: new Array<Submission>(),
    assignment: {} as Assignment
  };
  public dirListingNode: HTMLElement;
  public dirListing: DirListing;

  constructor(props: AssignmentProps) {
    super(props);
    this.state.assignment = props.assignment;
    this.index = props.index;
    this.lecture = props.lecture;

    this.toggleOpen = this.toggleOpen.bind(this);
    this.openFile = this.openFile.bind(this);
    this.fetchAssignment = this.fetchAssignment.bind(this);
    this.submitAssignment = this.submitAssignment.bind(this);
    this.getSubmissions = this.getSubmissions.bind(this);
    this.openFeedback = this.openFeedback.bind(this);
  }

  public componentWillReceiveProps(nextProps: AssignmentProps) {
    this.setState({ assignment: nextProps.assignment });  
  }

  public async componentDidMount() {
    this.getSubmissions();
    let renderer = new ExistingNodeRenderer(this.dirListingNode);
    let model = new FilterFileBrowserModel({
      auto: true,
      manager: GlobalObjects.docManager
    });

    const LISTING_CLASS = 'jp-FileBrowser-listing';
    this.dirListing = new DirListing({ model, renderer });
    this.dirListing.addClass(LISTING_CLASS);
    try {
      await model.cd(this.lecture.code);
      await model.cd(this.state.assignment.name);
    } catch (error) {
      console.log(error);
      return;
    }

    this.dirListingNode.onclick = async ev => {
      let model = this.dirListing.modelForClick(ev);
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
      let model = this.dirListing.modelForClick(ev);
      this.openFile(model.path);
    };
    this.dirListingNode.oncontextmenu = ev => {
      ev.preventDefault();
      ev.stopPropagation();
    };
  }

  private toggleOpen = (collapsable: string) => {
    if (collapsable == 'files') {
      this.setState({ filesOpen: !this.state.filesOpen });
    } else if (collapsable == 'submissions') {
      this.setState({ submissionsOpen: !this.state.submissionsOpen });
    }
  };

  private async openFile(path: string) {
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

  private async fetchAssignment() {
    const hasFiles = this.dirListing.model.items().next() !== undefined
    try {
      const type: Dialog.IResult<string> = await InputDialog.getItem({
        title: 'Select repository to fetch',
        items: ['release', "assignment"],
        current: hasFiles ? 1 : 0
      });
      if (!type.button.accept) return;
      const repoType = type.value;
      const confirm = await showDialog({
        title: 'Fetch Assignment',
        body: `Do you want to fetch ${this.state.assignment.name} from ${repoType}?`,
        buttons: [Dialog.cancelButton(), Dialog.okButton({ label: 'Fetch' })]
      });
      if (confirm.button.accept) {
        // update assignment
        await pullAssignment(
          this.lecture.id,
          this.state.assignment.id,
          repoType
        ).toPromise();
        await this.updateDirListing();
      }
    } catch (e) {
      showErrorMessage('Error Fetching Assignment', e);
    }
  }

  private async submitAssignment() {
    try {
      let result = await showDialog({
        title: 'Submit Assignment',
        body: `Do you want to submit ${this.state.assignment.name}? You can always re-submit the assignment before the due date.`,
        buttons: [Dialog.cancelButton({label: 'Cancel'}),Dialog.okButton({ label: 'Submit' })]
      });
      if (result.button.accept) {
        await submitAssignment(this.lecture, this.state.assignment).toPromise();
        await this.getSubmissions();
      }
    } catch (e) {
      showErrorMessage('Error Submitting Assignment', e);
    }
  }

  private getSubmissions() {
    getSubmissions(this.lecture, this.state.assignment).subscribe(
      userSubmissions =>
        this.setState({ submissions: userSubmissions.submissions }),
      error => showErrorMessage('Error Loading Submissions', error)
    );
  }

  private getSubmissionComponent() {
    if (this.state.submissions.length > 0) {
      return (
        <div className="assignment-content">
          {this.state.submissions.map((submission : Submission, i) => (
            <div className="submission-element">
              <Icon
                icon={IconNames.FORM}
                iconSize={this.iconSize}
                className="flavor-icon"
              ></Icon>
              {utcToLocalFormat(submission.submitted_at)}
              { submission.feedback_available ? (
                <Button
                  className="assignment-button"
                  icon={IconNames.CLOUD_DOWNLOAD}
                  active={true}
                  outlined={true}
                  intent={Intent.PRIMARY}
                  small={true}
                  onClick={ async () => {
                    (await pullFeedback(this.lecture,this.state.assignment,submission)).subscribe(
                      () => {this.openFeedback(this.lecture.id,this.state.assignment.id,submission.id)},
                      (e) => showErrorMessage("Error Fetching Feedback",e))
                  }
                }
                >
                  Open Feedback
                </Button>
              ) : null } 
              {i != this.state.submissions.length - 1 ? <Divider /> : null}
            </div>
          ))}
        </div>
      );
    } else {
      return <div className="assignment-content">No submissions yet!</div>;
    }
  }

  private openFeedback(lectureID: number, assignmentID: number, subID: number) {
    GlobalObjects.commands
      .execute('feedback:open', {
        lectureID,
        assignmentID,
        subID
      })
      .catch(error => {
        showErrorMessage('Error Opening Feedback View', error);
      });
  }

  public async updateDirListing() {
    let renderer = new ExistingNodeRenderer(this.dirListingNode);
    let model = new FilterFileBrowserModel({
      auto: true,
      manager: GlobalObjects.docManager
    });

    const LISTING_CLASS = 'jp-FileBrowser-listing';
    this.dirListing = new DirListing({ model, renderer });
    this.dirListing.addClass(LISTING_CLASS);
    try {
      await model.cd(this.lecture.code);
      await model.cd(this.state.assignment.name);
    } catch (error) {
      console.log(error);
      return;
    }
  }
  public render() {
    return (
      <li key={this.index}>
        <div className="assignment">
          <div className="assignment-header-container assignment-content">
            <span className="assignment-header-title">
            <Icon
              icon={IconNames.INBOX}
              iconSize={this.iconSize}
              className="flavor-icon"
            ></Icon>
            {this.state.assignment.name}
            {this.state.assignment.type === 'group' && (
              <Tag
                icon="people"
                intent="primary"
                className="assignment-tag"
                style={{ marginLeft: '10px' }}
              >
                Group
              </Tag>
            )}
            {this.state.assignment.status != 'released' && (
              <Tag
                icon="warning-sign"
                intent="danger"
                className="assignment-tag"
                style={{ marginLeft: '10px' }}
              >
                Not released for students
              </Tag>
            )}

            </span>
            <span className="assignment-header-button">
              <Button
                className="assignment-button"
                onClick={this.fetchAssignment}
                icon={IconNames.CLOUD_DOWNLOAD}
                disabled={this.state.assignment.status != 'released'}
                outlined
                intent={Intent.PRIMARY}
              >
                Fetch
              </Button>
              {this.state.assignment.type === "group" ? 
              <span>
                <Button intent='success' outlined className='assignment-button' icon="git-push">
                    Push
                </Button> 
                <Button intent='primary' outlined className='assignment-button' icon="git-pull">
                    Pull                  
                </Button> 
                </span>
              : null}
              <Button
                className="assignment-button"
                onClick={this.submitAssignment}
                icon={IconNames.SEND_MESSAGE}
                disabled={this.state.assignment.status == 'created'}
                outlined
                intent={Intent.SUCCESS}
              >
                Submit
              </Button>
              {this.state.assignment.due_date ? (
                <DeadlineComponent due_date={this.state.assignment.due_date} />
              ) : (
                <Tag intent="primary" style={{ marginLeft: '10px' }}>
                  No Deadline 😀
                </Tag>
              )}
            </span>
          </div>

          <div
            className='assignment-content'
            onClick={() => this.toggleOpen('files')
          }
          >
            <Icon
              icon={IconNames.CHEVRON_RIGHT}
              iconSize={this.iconSize}
              className={`collapse-icon-small ${
                this.state.filesOpen ? 'collapse-icon-small-open' : ''
              }`}
            ></Icon>
            <Icon
              icon={IconNames.FOLDER_CLOSE}
              iconSize={this.iconSize}
              className="flavor-icon"
            ></Icon>
            Exercises and Files
          </div>
          <Collapse isOpen={this.state.filesOpen} keepChildrenMounted={true}>
            <div
              className="assignment-dir-listing"
              ref={_element => (this.dirListingNode = _element)}
            ></div>
          </Collapse>

          <div
            className='assignment-content'
            onClick={() => this.toggleOpen('submissions')}
          >
            <Icon
              icon={IconNames.CHEVRON_RIGHT}
              iconSize={this.iconSize}
              className={`collapse-icon-small ${
                this.state.submissionsOpen ? 'collapse-icon-small-open' : ''
              }`}
            ></Icon>
            <Icon
              icon={IconNames.TICK_CIRCLE}
              iconSize={this.iconSize}
              className="flavor-icon"
            ></Icon>
            Submissions
          </div>
          <Collapse isOpen={this.state.submissionsOpen}>
            {this.getSubmissionComponent()}
          </Collapse>
        </div>
        <Divider />
      </li>
    );
  }
}
