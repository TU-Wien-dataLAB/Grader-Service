import * as React from "react";
import ReactDOM from "react-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import LocalizationProvider from "@mui/lab/LocalizationProvider";
import DateTimePicker from "@mui/lab/DateTimePicker";
import { Dialog } from "@material-ui/core";
import { DialogActions, DialogContent, DialogTitle, Paper, Stack, styled, TextFieldProps } from "@mui/material";
import { Assignment } from "../../model/assignment";

const validationSchema = yup.object({
  name: yup
    .string()
    .min(4, "Name should be 4-50 character length")
    .max(50, "Name should be 4-50 character length")
    .required("Name is required"),
  deadline: yup
    .date()
    .min( new Date(),"Deadline must be set in the future")
    .nullable()
    .required()

});

//TODO: props interface
export const EditDialog = (props : any) => {
  const [openDialog, setOpen] = React.useState(false);

  const formik = useFormik({
    initialValues: {
      name: props.assignment.name,
      deadline: new Date(props.assignment.due_date)
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      alert(JSON.stringify(values, null, 2));
      setOpen(false);
    }
  });


  return (
    <div>
      <Button
        variant="outlined"
        size="small"
        onClick={() => {
          setOpen(true);
        }}
      >
        Edit
      </Button>
      <Dialog open={openDialog}>
      <DialogTitle>Edit Assignment</DialogTitle>
        <form onSubmit={formik.handleSubmit}>
        <DialogContent>
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
            <DateTimePicker
              ampm={false}
              renderInput={(props : TextFieldProps) => {
                //@ts-ignore
                return <TextField {...props} helperText={formik.touched.deadline && formik.errors.deadline}
                error={formik.touched.deadline && Boolean(formik.errors.deadline)}
                />}}
              label="DateTimePicker"
              value={formik.values.deadline}
              onChange={(date) => {
                formik.setFieldValue("deadline", date);
              }}
            />
          </LocalizationProvider>
          </DialogContent>
          <DialogActions>
          <Button color="primary" variant="contained" type="submit">
            Submit
          </Button>
          <Button
            color="default"
            variant="outlined"
            onClick={() => {
              setOpen(false);
            }}
          >
            Cancel
          </Button>
          </DialogActions>
        </form>
      </Dialog>
    </div>
  );
};
//ReactDOM.render(<EditDialog />, document.getElementById("root"));
