import * as React from 'react';
import { Assignment } from '../model/assignment';
import { Icon, Collapse, Button, Tag } from '@blueprintjs/core'
import { GlobalObjects } from '../index';
import { showErrorMessage } from '@jupyterlab/apputils';
import { getAllSubmissions } from '../services/submissions.service';
import { Submission } from '../model/submission';


export interface AssignmentProps {
  index: number;
  lectureName: string;
  assignment: Assignment;
  lectureId: number;
}


export class CourseManageAssignmentComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lectureName: string;
  public lectureId: number;
  public index: number;
  public iconSize: number = 14;
  public state = {
    isOpen: true,
    submissions: new Array<Submission>(),
  };


  constructor(props: AssignmentProps) {
    super(props);
    this.assignment = props.assignment;
    this.index = props.index;
    this.lectureName = props.lectureName;
    this.lectureId = props.lectureId;
  }

  public componentDidMount() {
    // TODO: should only get all submissions if assignment is released
    getAllSubmissions({ id: this.lectureId }, { id: this.index }).subscribe(sub => {
      console.log(sub)
      this.setState(this.state.submissions = sub)
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
            <Button icon='search' outlined className="assignment-button">Preview</Button>
            <Button icon='learning' outlined className="assignment-button">Generate</Button>
            <Button icon='cloud-upload' outlined className="assignment-button">Release</Button>
            <Button icon='cloud-download' outlined className="assignment-button">Collect</Button>
            <Tag className="assignment-tag" icon="link">{this.state.submissions.length} Submissions</Tag>
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
          </div>
        </Collapse>
      </div>
    </li>
  }
}
