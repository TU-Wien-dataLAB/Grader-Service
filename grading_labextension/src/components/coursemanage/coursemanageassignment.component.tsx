import { Button, Collapse, Icon, Tag } from '@blueprintjs/core';
import { showErrorMessage } from '@jupyterlab/apputils';
import * as React from 'react';
import { GlobalObjects } from '../../index';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import { getAllSubmissions } from '../../services/submissions.service';


export interface AssignmentProps {
  index: number;
  lectureName: string;
  assignment: Assignment;
  lecture: Lecture;
}


export class CourseManageAssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lectureName: string;
  public lecture: Lecture;
  public index: number;
  public iconSize: number = 14;
  public state = {
    isOpen: false,
    submissions: new Array<Submission>(),
  };


  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
    this.lectureName = props.lectureName;
    this.lecture = props.lecture;
  }

  public componentDidMount() {
    // TODO: should only get all submissions if assignment is released
    getAllSubmissions(this.lecture , { id: this.index }).subscribe(userSubmissions => {
      console.log(userSubmissions)
      this.setState(this.state.submissions = userSubmissions.submissions)
    }
    )
  }

  private toggleOpen = () => {
    console.log("toggle assignment header")
    this.setState({ isOpen: !this.state.isOpen });
  }

  private openFile(path: string) {
    console.log("Opening file: " + path)
    GlobalObjects.commands.execute('docmanager:open', {
      path: path,
      options: {
        mode: 'tab-after' // tab-after tab-before split-bottom split-right split-left split-top
      }
    }).catch(error => {
      showErrorMessage("Error Opening File", error)
    })
  }

  private openGrading(lectureID: number, assignmentID: number) {
    GlobalObjects.commands.execute('grading:open', {
      lectureID,
      assignmentID
    }).catch(error => {
      showErrorMessage("Error Opening Submission View", error)
    })
  }

  private async openPreview(path: string) {
    //TODO: Should open preview file, opens the first original file right now
    this.openFile(path);
  }





  public render() {
    return <li key={this.index}>
      <div className="assignment">
        <div className="assignment-header">
          <span onClick={this.toggleOpen}>
            <Icon icon="chevron-right" iconSize={this.iconSize}
              className={`collapse-icon-small ${this.state.isOpen ? "collapse-icon-small-open" : ""}`}></Icon>
            <Icon icon="inbox" iconSize={this.iconSize} className="flavor-icon"></Icon>
            {this.assignment.name}
          </span>

          <span className="button-list">
            <Button icon='edit' outlined className="assignment-button">Edit</Button>
            <Button icon='build' outlined className="assignment-button">Generate</Button>
            <Button icon='search' outlined className="assignment-button" onClick={() => this.openPreview(`Informationsvisualisierung/${this.assignment.name}/${this.assignment.exercises.pop().name}`)} >Preview</Button>
            <Button icon='cloud-upload' outlined className="assignment-button" disabled={this.assignment.status=="created"}>Release</Button>
            <Button icon='cloud-download' outlined className="assignment-button" disabled={this.assignment.status=="created"}>Collect</Button>
            <Tag className="assignment-tag" icon="link" interactive onClick={() => this.openGrading(this.lecture.id, this.assignment.id)}>{this.state.submissions.length} Submissions</Tag>
          </span>
        </div>

        <Collapse isOpen={this.state.isOpen}>
          <div className="assignment-content">
            {this.assignment.exercises.map((ex, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${ex.name}`)}>
                <Icon icon="edit" iconSize={this.iconSize} className="flavor-icon"></Icon>
                {ex.name}
              </div>
            )}

            {this.assignment.files.map((file, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${file.name}`)}>
                <Icon icon="document" iconSize={this.iconSize} className="flavor-icon"></Icon>
                {file.name}
              </div>
            )}
            <span className="add-buttons">
              <Button icon="add" outlined className="assignment-button">Add File</Button>
              <Button icon="upload" outlined className="assignment-button">Upload File</Button>
            </span>
          </div>
        </Collapse>
      </div>
    </li>
  }
}
