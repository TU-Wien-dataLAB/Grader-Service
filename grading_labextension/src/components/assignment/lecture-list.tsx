import * as React from 'react';
import { getAllLectures } from '../../services/lectures.service';
import { Lecture } from '../../model/lecture';
import { Scope, UserPermissions } from '../../services/permission.service';
import { LectureComponent } from './lecture';

export interface ILectureListProps {
  root: HTMLElement;
}

export const LectureListComponent = (props: ILectureListProps): JSX.Element => {
  const [lectures, setLectures] = React.useState([] as Lecture[]);

  React.useEffect(() => {
    getAllLectures().then(lectures => {
      setLectures(lectures);
    });
  }, []);

  return (
    <div className="course-list">
      <h1>
        <p className="course-header">Assignments</p>
      </h1>
      {lectures
        .filter(el => UserPermissions.getScope(el) > Scope.student)
        .map((el, index) => (
          <LectureComponent lecture={el} root={props.root} open={index === 0} />
        ))}
    </div>
  );
};
