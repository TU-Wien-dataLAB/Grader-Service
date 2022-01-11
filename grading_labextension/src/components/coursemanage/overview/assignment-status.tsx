import {Assignment} from "../../../model/assignment";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Step,
  StepContent,
  StepLabel,
  Stepper,
  Typography
} from "@mui/material";
import Timeline from "@mui/lab/Timeline";
import * as React from "react";
import NewReleasesRoundedIcon from "@mui/icons-material/NewReleasesRounded";
import TaskIcon from '@mui/icons-material/Task';

import {AgreeDialog} from "../dialog";
import {updateAssignment} from "../../../services/assignments.service";
import {Lecture} from "../../../model/lecture";

export interface IAssignmentStatusProps {
  lecture: Lecture;
  assignment: Assignment;
  onAssignmentChange: (assignment: Assignment) => void;
  showAlert: (severity: string, msg: string) => void;
}

const getActiveStep = (status: Assignment.StatusEnum) => {
  switch (status) {
    case "created":
      return 0;
    case "pushed":
      return 1;
    case "released":
      return 2;
    case "complete":
      return 4;
  }
}

export const AssignmentStatus = (props: IAssignmentStatusProps) => {
  const [assignment, setAssignment] = React.useState(props.assignment);
  const [showDialog, setShowDialog] = React.useState(false);
  const [dialogContent, setDialogContent] = React.useState({
    title: '',
    message: '',
    handleAgree: null,
    handleDisagree: null
  });
  const closeDialog = () => setShowDialog(false);

  const steps = [
    {
      label: 'Created',
      description: <Typography sx={{fontSize: 12}}>The assignment has been created and files can now be added to be
        pushed. By pushing files
        you will progress to the next step.</Typography>,
    },
    {
      label: 'Pushed',
      description:
        <Box>
          <Typography sx={{fontSize: 12}}>Files have been pushed to the source repository. If you are happy with
            the assignments you can release them or make further changes to the files and push them again!</Typography>
          <Button
            sx={{mt: 1}}
            onClick={() => handleReleaseAssignment()}
            variant="outlined"
            size="small"
          >
            <NewReleasesRoundedIcon fontSize="small" sx={{mr: 1}}/>
            Release
          </Button>
        </Box>,
    },
    {
      label: 'Released',
      description:
        <Box>
          <Typography sx={{fontSize: 12}}>The assignment has been released to students and it is not advised to
            push further changes since this would probably reset most of the students progress.
            If the assignment is over you can mark it as complete
            in the edit menu or right here.</Typography>
          <Button
            sx={{mt: 1}}
            onClick={() => completeAssignment()}
            variant="outlined"
            size="small"
          >
            <TaskIcon fontSize="small" sx={{mr: 1}}/>
            Complete
          </Button>
        </Box>,
    },
    {
      label: 'Assignment Completed',
      description: <Typography sx={{fontSize: 12}}>The assignment has been completed and is not visible to students
        anymore. You can change the status in the edit menu.</Typography>,
    }
  ];

  const handleReleaseAssignment = async () => {
    setDialogContent({
      title: 'Release Assignment',
      message: `Do you want to release ${assignment.name} for all students?`,
      handleAgree: () => {
        setDialogContent({
          title: 'Confirmation',
          message: `Are you sure you want to release ${assignment.name}?`,
          handleAgree: async () => {
            try {
              console.log('releasing assignment');
              let a = assignment;
              a.status = 'released';
              a = await updateAssignment(props.lecture.id, a);
              setAssignment(a);
              props.onAssignmentChange(a);
              props.showAlert('success', 'Successfully Released Assignment');
            } catch (err) {
              props.showAlert('error', 'Error Releasing Assignment');
            }
            closeDialog();
          },
          handleDisagree: () => closeDialog()
        });
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  const completeAssignment = async () => {
    setDialogContent({
      title: 'Complete Assignment',
      message: `Do you want to mark ${assignment.name} as complete?`,
      handleAgree: async () => {
        try {
          let a = assignment;
          a.status = 'complete';
          a = await updateAssignment(props.lecture.id, a);
          setAssignment(a);
          props.onAssignmentChange(a);
          props.showAlert('success', 'Successfully Updated Assignment');
        } catch (err) {
          props.showAlert('error', 'Error Updating Assignment');
        }
        closeDialog();
      },
      handleDisagree: () => closeDialog()
    });
    setShowDialog(true);
  };

  return (
    <Card elevation={3} className='flexbox-item'>
      <CardHeader title="Assignment Status"/>
      <CardContent sx={{height: '300px', width: '300px', overflowY: "auto"}}>
        <Stepper activeStep={getActiveStep(assignment.status)} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel
                optional={
                  index === 3 ? (
                    <Typography variant="caption">Last step</Typography>
                  ) : null
                }
              >
                {step.label}
              </StepLabel>
              <StepContent>
                <Typography>{step.description}</Typography>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </CardContent>
      <AgreeDialog open={showDialog} {...dialogContent} />
    </Card>
  );
}