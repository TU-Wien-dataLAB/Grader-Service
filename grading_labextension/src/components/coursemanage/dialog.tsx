import React from "react";
import ReactDOM from "react-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
//import { DateTimePicker } from "@material-ui/core";
import { Dialog } from "@material-ui/core";

const validationSchema = yup.object({
  name: yup
    .string()
    .min(4, "Name should be 4-100 character length")
    .max(100, "Name should be 4-100 character length")
    .required("Name is required"),
  deadline: yup.string()
});

export const EditDialog = () => {
  const formik = useFormik({
    initialValues: {
      name: "yo",
      deadline: "foobar"
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      alert(JSON.stringify(values, null, 2));
    }
  });

  return (
    <div>
      <Dialog open>
        <form onSubmit={formik.handleSubmit}>
          <TextField
            fullWidth
            id="name"
            name="name"
            label="Assignment Name"
            value={formik.values.name}
            onChange={formik.handleChange}
            error={formik.touched.name && Boolean(formik.errors.name)}
            helperText={formik.touched.name && formik.errors.name}
          />
          <TextField
            fullWidth
            id="deadline"
            name="deadline"
            label="Set deadline"
            value={formik.values.deadline}
            onChange={formik.handleChange}
            error={formik.touched.deadline && Boolean(formik.errors.deadline)}
            helperText={formik.touched.deadline && formik.errors.deadline}
          />{" "}
          <Button color="primary" variant="contained" fullWidth type="submit">
            Submit
          </Button>
        </form>
      </Dialog>
    </div>
  );
};
ReactDOM.render(<EditDialog />, document.getElementById("root"));