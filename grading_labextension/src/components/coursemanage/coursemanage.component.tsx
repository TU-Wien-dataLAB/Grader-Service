import * as React from 'react';
import { Lecture } from '../../model/lecture';
import { getAllLectures } from '../../services/lectures.service';
import { Scope, UserPermissions } from '../../services/permission.service';
import { showErrorMessage } from '@jupyterlab/apputils';
import { LectureComponent } from './lecture';

export interface CourseManageProps {
  // lectures: Array<Lecture>;
  root: HTMLElement;
}

export class CourseManageComponent extends React.Component<CourseManageProps> {
  public state = {
    lectures: new Array<Lecture>()
  };

  constructor(props: CourseManageProps) {
    super(props);
    // this.state = {"lectures": props.lectures};
  }

  public async componentWillMount() {
    try {
      await UserPermissions.loadPermissions();
    } catch (err) {
      showErrorMessage('Error Loading Permissions', err);
    }
    getAllLectures().then(l => {
      this.setState({ lectures: l });
    });
  }

  public render() {
    return (
      <div className="course-list">
        <h1>
          <p className="course-header">Course Management</p>
        </h1>
        {this.state.lectures
          .filter(el => UserPermissions.getScope(el) > Scope.student)
          .map((el, index) => (
            <LectureComponent lecture={el} root={this.props.root} />
          ))}
      </div>
    );
  }
}
