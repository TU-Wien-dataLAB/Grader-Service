import * as React from 'react';
import ReactDOM from 'react-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';

import AdapterDateFns from '@mui/lab/AdapterDateFns';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import DateTimePicker from '@mui/lab/DateTimePicker';
import {
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  Stack,
  styled,
  TextFieldProps,
  DialogContentText,
  IconButton,
  Checkbox,
  FormControlLabel,
  InputLabel,
  Select,
  MenuItem,
  Radio
} from '@mui/material';
import { Assignment } from '../../model/assignment';
import { LoadingButton } from '@mui/lab';
import EditIcon from '@mui/icons-material/Edit';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import {
  createAssignment,
  updateAssignment
} from '../../services/assignments.service';
import { Lecture } from '../../model/lecture';
import TypeEnum = Assignment.TypeEnum;
import { updateLecture } from '../../services/lectures.service';

const validationSchema = yup.object({
  name: yup
    .string()
    .min(4, 'Name should be 4-50 character length')
    .max(50, 'Name should be 4-50 character length')
    .required('Name is required'),
  due_date: yup
    .date()
    .min(new Date(), 'Deadline must be set in the future')
    .nullable(),
  type: yup
    .mixed()
    .oneOf(['user', 'group']),
  automatic_grading: yup
    .boolean()
});

export interface IEditDialogProps {
  lecture: Lecture;
  assignment: Assignment;
}

export const EditDialog = (props: IEditDialogProps) => {
  const formik = useFormik({
    initialValues: {
      name: props.assignment.name,
      due_date:
        props.assignment.due_date !== null
          ? new Date(props.assignment.due_date)
          : null,
      type: props.assignment.type,
      automatic_grading: props.assignment.automatic_grading
    },
    validationSchema: validationSchema,
    onSubmit: values => {
      const updatedAssignment: Assignment = Object.assign(
        props.assignment,
        values
      );
      console.log(updatedAssignment);
      //TODO: either need lect id from assignment or need lecture hear
      updateAssignment(props.lecture.id, updatedAssignment);
      setOpen(false);
    }
  });

  const [openDialog, setOpen] = React.useState(false);

  return (
    <div>
      <IconButton
        sx={{ mt: -1 }}
        onClick={e => {
          e.stopPropagation();
          setOpen(true);
        }}
        onMouseDown={event => event.stopPropagation()}
        aria-label="edit"
      >
        <EditIcon />
      </IconButton>
      <Dialog open={openDialog} onBackdropClick={() => setOpen(false)}>
        <DialogTitle>Edit Assignment</DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Stack spacing={2}>
              <TextField
                variant="outlined"
                fullWidth
                id="name"
                name="name"
                label="Assignment Name"
                value={formik.values.name}
                onChange={formik.handleChange}
                error={formik.touched.name && Boolean(formik.errors.name)}
                helperText={formik.touched.name && formik.errors.name}
              />

              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <FormControlLabel
                  control={
                    <Checkbox
                      value={props.assignment.due_date !== null ? true : false}
                      onChange={async e => {
                        console.log('Before: ' + formik.values.due_date);
                        if (e.target.checked) {
                          await formik.setFieldValue('due_date', new Date());
                        } else {
                          await formik.setFieldValue('due_date', null);
                        }
                        console.log('After: ' + formik.values.due_date);
                      }}
                    />
                  }
                  label="Set Deadline"
                />

                <DateTimePicker
                  ampm={false}
                  disabled={formik.values.due_date === null}
                  renderInput={(props: TextFieldProps) => {
                    //@ts-ignore
                    return (
                      <TextField
                        {...props}
                        helperText={
                          formik.touched.due_date && formik.errors.due_date
                        }
                        error={
                          formik.touched.due_date &&
                          Boolean(formik.errors.due_date)
                        }
                      />
                    );
                  }}
                  label="DateTimePicker"
                  value={formik.values.due_date}
                  onChange={date => {
                    formik.setFieldValue('due_date', date);
                  }}
                />
              </LocalizationProvider>

              <FormControlLabel
                  control={
                    <Checkbox
                      id='automatic_graded'
                      name='automatic_graded'
                      value={formik.values.automatic_grading}
                      checked={formik.values.automatic_grading}
                      onChange={e => {
                        if (e.target.checked) {
                          formik.setFieldValue('automatic_grading', true);
                        } else {
                          formik.setFieldValue('automatic_grading', false);
                        }
                      }}
                    />
                  }
                  label="Grade submissions automatically"
                />

              <InputLabel id="demo-simple-select-label">Type</InputLabel>
              <Select
                labelId="assignment-type-select-label"
                id="assignment-type-select"
                value={formik.values.type}
                label="Type"
                onChange={e => {
                  formik.setFieldValue('type', e.target.value);
                }}
              >
                <MenuItem value={'user'}>User</MenuItem>
                <MenuItem value={'group'}>Group</MenuItem>
              </Select>

              <Button
                fullWidth
                color="error"
                variant="contained"
                onClick={() => {
                  setOpen(false);
                }}
              >
                Delete Assignment
              </Button>
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button
              color="primary"
              variant="outlined"
              onClick={() => {
                setOpen(false);
              }}
            >
              Cancel
            </Button>

            <Button color="primary" variant="contained" type="submit">
              Submit
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </div>
  );
};

const validationSchemaLecture = yup.object({
  name: yup
    .string()
    .min(4, 'Name should be 4-50 characters long')
    .max(50, 'Name should be 4-50 characters long')
    .required('Name is required'),
  semester: yup
    .string()
    .min(4, 'Semester should be 4-12 characters long')
    .max(12, 'Semester should be 4-12 characters long')
    .required('Lecture code is required'),
  complete: yup
    .boolean()
});

export interface IEditLectureProps {
  lecture: Lecture;
  handleSubmit: () => void;
}

export const EditLectureDialog = (props: IEditLectureProps) => {
  const formik = useFormik({
    initialValues: {
      name: props.lecture.name,
      semester: props.lecture.semester,
      complete: props.lecture.complete
    },
    validationSchema: validationSchemaLecture,
    onSubmit: values => {
      const updatedLecture: Lecture = Object.assign(props.lecture, values);
      console.log(updatedLecture);
      updateLecture(updatedLecture)
        .then(props.handleSubmit)
        .catch(error => console.log(error));
      setOpen(false);
    }
  });

  const [openDialog, setOpen] = React.useState(false);

  return (
    <div>
      <IconButton
        sx={{ mt: -1 }}
        onClick={e => {
          e.stopPropagation();
          setOpen(true);
        }}
        onMouseDown={event => event.stopPropagation()}
        aria-label="edit"
      >
        <EditIcon />
      </IconButton>
      <Dialog open={openDialog} onBackdropClick={() => setOpen(false)}>
        <DialogTitle>Edit Lecture</DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Stack spacing={2}>
              <TextField
                variant="outlined"
                fullWidth
                id="name"
                name="name"
                label="Lecture Name"
                value={formik.values.name}
                onChange={formik.handleChange}
                error={formik.touched.name && Boolean(formik.errors.name)}
                helperText={formik.touched.name && formik.errors.name}
              />
              <TextField
                variant="outlined"
                fullWidth
                id="semester"
                name="semester"
                label="Semester"
                value={formik.values.semester}
                onChange={formik.handleChange}
                error={
                  formik.touched.semester && Boolean(formik.errors.semester)
                }
                helperText={formik.touched.semester && formik.errors.semester}
              />
              <FormControlLabel
                control={
                  <Checkbox
                    value={props.lecture.complete}
                    onChange={e => {
                      formik.setFieldValue('complete', e.target.checked);
                    }}
                  />
                }
                label="Complete"
              />
              <Button
                fullWidth
                color="error"
                variant="contained"
                onClick={() => {
                  setOpen(false);
                }}
              >
                Delete Lecture
              </Button>
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button
              color="primary"
              variant="outlined"
              onClick={() => {
                setOpen(false);
              }}
            >
              Cancel
            </Button>

            <Button color="primary" variant="contained" type="submit">
              Submit
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </div>
  );
};

interface ICreateDialogProps {
  lecture: Lecture;
  handleSubmit: () => void;
}

export const CreateDialog = (props: ICreateDialogProps) => {
  const formik = useFormik({
    initialValues: {
      name: 'Assignment',
      due_date: null,
      type: 'user',
      automatic_grading: false
    },
    validationSchema: validationSchema,
    onSubmit: values => {
      const updatedAssignment: Assignment = {
        name: values.name,
        due_date: values.due_date,
        type: values.type as TypeEnum,
        automatic_grading: values.automatic_grading
      };
      console.log(updatedAssignment);
      //TODO: either need lect id from assignment or need lecture hear
      createAssignment(props.lecture.id, updatedAssignment);
      setOpen(false);
      props.handleSubmit();
    }
  });

  const [openDialog, setOpen] = React.useState(false);

  return (
    <div>
      <Button
        sx={{ mt: -1 }}
        onClick={e => {
          e.stopPropagation();
          setOpen(true);
        }}
        onMouseDown={event => event.stopPropagation()}
        aria-label="create"
        size={'small'}
      >
        <AddRoundedIcon /> New Assignment
      </Button>
      <Dialog open={openDialog} onBackdropClick={() => setOpen(false)}>
        <DialogTitle>Edit Assignment</DialogTitle>
        <form onSubmit={formik.handleSubmit}>
          <DialogContent>
            <Stack spacing={2}>
              <TextField
                variant="outlined"
                fullWidth
                id="name"
                name="name"
                label="Assignment Name"
                value={formik.values.name}
                onChange={formik.handleChange}
                error={formik.touched.name && Boolean(formik.errors.name)}
                helperText={formik.touched.name && formik.errors.name}
              />

              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <FormControlLabel
                  control={
                    <Checkbox
                      value={false}
                      onChange={async e => {
                        console.log('Before: ' + formik.values.due_date);
                        if (e.target.checked) {
                          await formik.setFieldValue('due_date', new Date());
                        } else {
                          await formik.setFieldValue('due_date', null);
                        }
                        console.log('After: ' + formik.values.due_date);
                      }}
                    />
                  }
                  label="Set Deadline"
                />

                <DateTimePicker
                  ampm={false}
                  disabled={formik.values.due_date === null}
                  renderInput={(props: TextFieldProps) => {
                    //@ts-ignore
                    return (
                      <TextField
                        {...props}
                        helperText={
                          formik.touched.due_date && formik.errors.due_date
                        }
                        error={
                          formik.touched.due_date &&
                          Boolean(formik.errors.due_date)
                        }
                      />
                    );
                  }}
                  label="DateTimePicker"
                  value={formik.values.due_date}
                  onChange={date => {
                    formik.setFieldValue('due_date', date);
                  }}
                />
              </LocalizationProvider>
              
              <FormControlLabel
                  control={
                    <Checkbox
                      id='automatic_graded'
                      name='automatic_graded'
                      checked={formik.values.automatic_grading}
                      value={formik.values.automatic_grading}
                      onChange={e => {
                        if (e.target.checked) {
                          formik.setFieldValue('automatic_grading', true);
                        } else {
                          formik.setFieldValue('automatic_grading', false);
                        }
                      }}
                    />
                  }
                  label="Grade submissions automatically"
                />

              <InputLabel id="demo-simple-select-label">Type</InputLabel>
              <Select
                labelId="assignment-type-select-label"
                id="assignment-type-select"
                value={formik.values.type}
                label="Type"
                onChange={e => {
                  formik.setFieldValue('type', e.target.value);
                }}
              >
                <MenuItem value={'user'}>User</MenuItem>
                <MenuItem value={'group'}>Group</MenuItem>
              </Select>
            </Stack>
          </DialogContent>
          <DialogActions>
            <Button
              color="primary"
              variant="outlined"
              onClick={() => {
                setOpen(false);
              }}
            >
              Cancel
            </Button>

            <Button color="primary" variant="contained" type="submit">
              Create
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </div>
  );
};

export interface IAgreeDialogProps {
  open: boolean;
  title: string;
  message: string;
  handleAgree: () => void;
  handleDisagree: () => void;
}

export const AgreeDialog = (props: IAgreeDialogProps) => {
  const [loading, setLoading] = React.useState(false);

  const executeAction = async (action: () => void) => {
    setLoading(true);
    await action();
    setLoading(false);
  };

  return (
    <Dialog
      open={props.open}
      onClose={props.handleDisagree}
      onBackdropClick={props.handleDisagree}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{props.title}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          {props.message}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleDisagree}>Disagree</Button>
        <LoadingButton
          loading={loading}
          onClick={() => executeAction(props.handleAgree)}
          autoFocus
        >
          Agree
        </LoadingButton>
      </DialogActions>
    </Dialog>
  );
};
//ReactDOM.render(<EditDialog />, document.getElementById("root"));
