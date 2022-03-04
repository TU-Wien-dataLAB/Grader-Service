import * as React from 'react';
import {Lecture} from '../../model/lecture';
import {getAllLectures} from '../../services/lectures.service';
import {Scope, UserPermissions} from '../../services/permission.service';
import {showErrorMessage} from '@jupyterlab/apputils';
import {LectureComponent} from './lecture';
import {AlertProps, Portal, Snackbar} from "@mui/material";
import MuiAlert from "@mui/material/Alert";

export interface CourseManageProps {
  // lectures: Array<Lecture>;
  root: HTMLElement;
}

export const CourseManageComponent = (props: CourseManageProps) => {
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

  const [lectures, setLectures] = React.useState([] as Lecture[]);
  React.useEffect(() => {
    UserPermissions.loadPermissions()
      .then(() => {
        getAllLectures().then(l => setLectures(l))
      })
      .catch(() => showAlert("error", "Error Loading Permissions"))
  }, [props])

  return (
    <div className="course-list">
      <h1>
        <p className="course-header">Course Management</p>
      </h1>
      {lectures
        .filter(el => UserPermissions.getScope(el) > Scope.student)
        .map((el, index) => (
          <LectureComponent lecture={el} root={props.root} showAlert={showAlert}/>
        ))}
      <Portal container={document.body}>
        <Snackbar
          open={alert}
          onClose={handleAlertClose}
          sx={{mb: 2, ml: 2}}
        >
          <MuiAlert
            onClose={handleAlertClose}
            severity={severity as AlertProps['severity']}
            sx={{width: '100%'}}
          >
            {alertMessage}
          </MuiAlert>
        </Snackbar>
      </Portal>
    </div>
  );
}
