import * as React from 'react';
import {Lecture} from '../../model/lecture';
import {getAllLectures} from '../../services/lectures.service';
import {Scope, UserPermissions} from '../../services/permission.service';
import {showErrorMessage} from '@jupyterlab/apputils';
import {LectureComponent} from './lecture';

export interface CourseManageProps {
  // lectures: Array<Lecture>;
  root: HTMLElement;
}

export const CourseManageComponent = (props: CourseManageProps) => {
  const [lectures, setLectures] = React.useState([] as Lecture[]);
  React.useEffect(() => {
    UserPermissions.loadPermissions()
      .then(() => {
        getAllLectures().then(l => setLectures(l))
      })
      .catch((err) => console.log(err))
  }, [props])

  return (
    <div className="course-list">
      <h1>
        <p className="course-header">Course Management</p>
      </h1>
      {lectures
        .filter(el => UserPermissions.getScope(el) > Scope.student)
        .map((el, index) => (
          <LectureComponent lecture={el} root={props.root}/>
        ))}
    </div>
  );
}
