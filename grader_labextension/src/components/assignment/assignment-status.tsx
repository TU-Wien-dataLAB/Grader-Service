// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import { Assignment } from '../../model/assignment';
import {
  Card,
  CardContent,
  Step,
  StepLabel,
  Stepper,
  Typography
} from '@mui/material';
import * as React from 'react';
import { getFiles } from '../../services/file.service';

import { Lecture } from '../../model/lecture';
import { Submission } from '../../model/submission';
import ChatRoundedIcon from '@mui/icons-material/ChatRounded';
/**
 * Props for AssignmentComponent.
 */
export interface IAssignmentStatusProps {
  lecture: Lecture;
  assignment: Assignment;
  submissions: Submission[];
}

/**
 * Renders the assignment status stepper.
 * @param props props of assignment status component
 */
export const AssignmentStatus = (props: IAssignmentStatusProps) => {
  const [activeStep, setActiveStep] = React.useState(0);

  /**
   * Calculates what the current step of the student assignment is.
   */
  const getActiveStep = async () => {
    const hasFeedback = props.submissions.reduce(
      (accum: boolean, curr: Submission) => accum || curr.feedback_available,
      false
    );
    if (hasFeedback) {
      return 3;
    }
    if (props.submissions.length > 0) {
      return 1;
    }
    return 0;
  };

  const fontSize = 14;
  const steps = [
    {
      label: 'Pulled',
      description: (
        <Typography sx={{ fontSize }}>
          You pulled from the release repository and can now work on the
          assignment. If you are happy with your solution you can submit it.
          Before the deadline you can always resubmit until you are happy with
          the solution.
        </Typography>
      )
    },
    {
      label: 'Submitted',
      description: (
        <Typography sx={{ fontSize }}>
          You have submitted the assignment {props.submissions.length} time
          {props.submissions.length == 1 ? '' : 's'}. The instructor can review
          each submission, but will most likely prioritise the latest.
        </Typography>
      )
    },
    {
      label: 'Feedback available',
      description: (
        <Typography sx={{ fontSize }}>
          You received feedback for one or more of your submissions! You can
          view the feedback in the list of submission when clicking on the{' '}
          <ChatRoundedIcon sx={{ fontSize }} /> icon. Within the deadline you
          can make more submissions, regardless of whether you already received
          feedback.
        </Typography>
      )
    }
  ];
  getActiveStep().then(s => setActiveStep(s));

  return (
    <Card elevation={0}>
      <CardContent sx={{ overflowY: 'auto' }}>
        <Stepper activeStep={activeStep} orientation="horizontal">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel>{step.label}</StepLabel>
            </Step>
          ))}
        </Stepper>
        <Typography sx={{ mt: 2, ml: 2, maxWidth: '50%' }}>
          {steps[activeStep < 2 ? activeStep : 2].description}
        </Typography>
      </CardContent>
    </Card>
  );
};
