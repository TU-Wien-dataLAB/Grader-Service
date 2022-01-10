import {ModalTitle} from "../util/modal-title";
import {Box, Typography} from "@mui/material";
import * as React from "react";
import {Lecture} from "../../model/lecture";
import {Assignment} from "../../model/assignment";
import {Submission} from "../../model/submission";

export interface IManualGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  submission: Submission;
}

export const ManualGrading = (props: IManualGradingProps) => {
  React.useEffect(() => {
    console.log("pulling autograding results");
  }, [props])

  return (
    <Box>
      <ModalTitle title={"Manual Grading " + props.assignment.name}/>
      <Box sx={{m: 2, mt: 12}}>
        <Typography>
          {props.submission.commit_hash}
        </Typography>
      </Box>
    </Box>
  )
}