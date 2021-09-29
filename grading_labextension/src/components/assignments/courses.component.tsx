import * as React from 'react';
import { AssignmentsComponent } from './assignment-list.component';
import { Lecture } from '../../model/lecture';
import { getAllLectures } from '../../services/lectures.service';
import { showErrorMessage } from '@jupyterlab/apputils';
import { UserPermissions } from '../../services/permission.service';
import { Button, Intent } from '@blueprintjs/core';
import { IconNames } from '@blueprintjs/icons';

export interface CoursesProps {
  // lectures: Array<Lecture>;
}

export class CoursesComponent extends React.Component<CoursesProps> {
  public lectures: number[];
  public state = {
    lectures: new Array<Lecture>()
  };
  public assignmentComponents: Array<AssignmentsComponent> = [];

  constructor(props: CoursesProps) {
    super(props);
  }

  public async componentDidMount() {
    this.getLectures();
  }

  public async getLectures() {
    getAllLectures().subscribe(
      lectures => this.setState({ lectures }),
      error => showErrorMessage('Error Fetching Lectures', error)
    );
    try {
      await UserPermissions.loadPermissions();
    } catch (err) {
      showErrorMessage('Error Loading Permissions', err);
    }
    console.log('User permissions:');
    console.log(UserPermissions.getPermissions());
  }


  private reload() {
    this.assignmentComponents.map(v => {
      v?.loadAssignments();
    });
  }


  public render() {
    return (
      <div className="course-list">
        <div id="assignment-header">
          <h1>
            <p>Assignments</p>
          </h1>
          <Button id="reload-button" className="assignment-button" onClick={() => this.reload()} icon={IconNames.REFRESH} outlined intent={Intent.SUCCESS}>Reload</Button>
        </div>
        {this.state.lectures.map((el, index) => (
          <AssignmentsComponent lecture={el} open={index == 0} ref={(r) => this.assignmentComponents.push(r)} />
        ))}
      </div>
    );
  }
}
