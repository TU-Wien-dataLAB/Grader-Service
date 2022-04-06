import * as React from 'react';
import { getAllLectures } from '../../services/lectures.service';
import { Lecture } from '../../model/lecture';
import { LectureComponent } from './lecture';
import { AlertProps, Snackbar, Portal } from '@mui/material';
import MuiAlert from '@mui/material/Alert';

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
        <Snackbar open={alert} onClose={handleAlertClose} sx={{ mb: 2, ml: 2 }}>
          <MuiAlert
            onClose={handleAlertClose}
            severity={severity as AlertProps['severity']}
            sx={{ width: '100%' }}
          >
            {alertMessage}
          </MuiAlert>
        </Snackbar>
      </Portal>
    </div>
  );
};
