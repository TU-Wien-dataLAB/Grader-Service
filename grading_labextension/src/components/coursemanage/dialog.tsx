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
  FormControlLabel
} from '@mui/material';
import { Assignment } from '../../model/assignment';
import { LoadingButton } from '@mui/lab';
import EditIcon from '@mui/icons-material/Edit';
import { updateAssignment } from '../../services/assignments.service';


const validationSchema = yup.object({
  name: yup
    .string()
    .min(4, 'Name should be 4-50 character length')
    .max(50, 'Name should be 4-50 character length')
    .required('Name is required'),
  due_date: yup
    .date()
    .min(new Date(), 'Deadline must be set in the future')
    .nullable()
});

export interface IEditDialogProps {
  assignment: Assignment;
}

//TODO: props interface
export const EditDialog = (props: IEditDialogProps) => {
  

  const formik = useFormik({
    enableReinitialize
    initialValues: {
      name: props.assignment.name,
      due_date: props.assignment.due_date != null ? new Date(props.assignment.due_date) : null
    },
    validationSchema: validationSchema,
    onSubmit: values => {
      const updatedAssignment : Assignment = Object.assign(props.assignment,values);
      console.log(updatedAssignment);
      //TODO: either need lect id from assignment or need lecture hear
      //updateAssignment(updatedAssignment.lect_id,updatedAssignment);
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
      <Dialog open={openDialog}>
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
                value={props.assignment.due_date != null ? true : false} 
                onChange={
                  async (e) => {
                    console.log("Before: "+formik.values.due_date);
                    if(e.target.checked) {
                      await formik.setFieldValue('due_date', new Date())
                    } else {
                      await formik.setFieldValue('due_date', null) 
                    }
                    console.log("After: "+formik.values.due_date)

                  }
                } 
              />}
              label="Set Deadline"/>

            { formik.values.due_date != null
              &&
              <DateTimePicker
                ampm={false}
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
              }

            </LocalizationProvider>

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
