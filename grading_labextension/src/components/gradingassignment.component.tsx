import * as React from 'react';
import { Assignment } from '../model/assignment';
import { Button } from '@jupyterlab/ui-components';
import { Icon,Collapse } from '@blueprintjs/core'
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


export class AssignmentGradingComponent extends React.Component<AssignmentProps> {
  public assignment: Assignment;
  public lectureName: string;
  public lectureId: number;
  public index: number;
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
    getAllSubmissions({id:this.lectureId},{id:this.index}).subscribe(sub => {
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
        <div onClick={this.toggleOpen} className="assignment-header">
          <Icon icon="chevron-right" iconSize={12}
            className={`collapse-icon-small ${this.state.isOpen ? "collapse-icon-small-open" : ""}`}></Icon>
          <Icon icon="inbox" iconSize={12} className="flavor-icon"></Icon>
          {this.assignment.name} 
          
          <Button icon='edit' minimal></Button>
          <Button icon='search' minimal></Button>
          <Button icon='learning' minimal></Button>
          <Button icon='cloud-upload' minimal></Button>
          <Button icon='cloud-download' minimal></Button>
          Submission count: {this.state.submissions.length}
        </div>
       
        <Collapse isOpen={this.state.isOpen}>
          <div className="assignment-content">
            {this.assignment.exercises.map((ex, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${ex.name}`)}>
                <Icon icon="edit" iconSize={12} className="flavor-icon"></Icon>
                {ex.name}
              </div>
            )}

            {this.assignment.files.map((file, i) =>
              <div className="list-element" onClick={() => this.openFile(`${this.lectureName}/${this.assignment.name}/${file.name}`)}>
                <Icon icon="document" iconSize={12} className="flavor-icon"></Icon>
                {file.name}
              </div>
            )}
          </div>
        </Collapse>
      </div>
    </li>
  }
}
