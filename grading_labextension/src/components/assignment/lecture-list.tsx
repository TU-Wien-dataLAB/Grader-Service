import * as React from 'react';
import { getAllLectures } from '../../services/lectures.service';
import { Lecture } from '../../model/lecture';
import { LectureComponent } from './lecture';
import { AlertProps, Alert, Portal, AlertTitle } from '@mui/material';

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

  const [alert, setAlert] = React.useState(false);
  const [severity, setSeverity] = React.useState('success');
  const [alertMessage, setAlertMessage] = React.useState('');

  const showAlert = (severity: string, msg: string) => {
    setSeverity(severity);
    setAlertMessage(msg);
    setAlert(true);
  };

  const handleAlertClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === 'clickaway') {
      return;
    }
    setAlert(false);
  };

  return (
    <div className="course-list">
      <h1>
        <p className="course-header">Assignments</p>
      </h1>
      {lectures.map((el, index) => (
        <LectureComponent
          lecture={el}
          root={props.root}
          open={true}
          showAlert={showAlert}
        />
      ))}
      <Portal container={document.body}>
        {alert && (
          <Alert
            onClose={handleAlertClose}
            severity={severity as AlertProps['severity']}
            sx={{ position: 'fixed', left: '50%', ml: '-50px', mt: 10 }}
          >
            <AlertTitle>{alertMessage}</AlertTitle>
          </Alert>
        )}
      </Portal>
    </div>
  );
};
