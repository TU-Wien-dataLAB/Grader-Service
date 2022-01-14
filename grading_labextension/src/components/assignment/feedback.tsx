import {ModalTitle} from "../util/modal-title";
import {Box, Stack, Typography} from "@mui/material";
import * as React from "react";
import {Lecture} from "../../model/lecture";
import {Assignment} from "../../model/assignment";
import {Submission} from "../../model/submission";
import {getProperties, pullFeedback} from "../../services/submissions.service";
import {GradeBook} from "../../services/gradebook";
import {FilesList} from "../util/file-list";

export interface IFeedbackProps {
  lecture: Lecture;
  assignment: Assignment;
  submission: Submission;
}

export const Feedback = (props: IFeedbackProps) => {
  const [gradeBook, setGradeBook] = React.useState(null);
  const [path, setPath] = React.useState(null);

  React.useEffect(() => {
    getProperties(props.lecture.id, props.assignment.id, props.submission.id).then((properties) => {
      const gradeBook = new GradeBook(properties);
      setGradeBook(gradeBook);
    });
    pullFeedback(props.lecture, props.assignment, props.submission).then(() => {
      const feedbackPath = `feedback/${props.lecture.code}/${props.assignment.name}/${props.submission.id}`
      setPath(feedbackPath);
    });
  }, [props])

  return (
    <Box>
      <ModalTitle title={"Feedback for " + props.assignment.name}/>
      <Box sx={{m: 2, mt: 12}}>
        <Stack direction="row" spacing={2} sx={{ml: 2}}>
          <Stack  sx={{mt: 0.5}}>
            <Typography textAlign="right" color="text.secondary" sx={{fontSize: 12, height: 35}}>
              Lecture
            </Typography>
            <Typography textAlign="right" color="text.secondary" sx={{fontSize: 12, height: 35}}>
              Assignment
            </Typography>
            <Typography textAlign="right" color="text.secondary" sx={{fontSize: 12, height: 35}}>
              Points
            </Typography>
            <Typography textAlign="right" color="text.secondary" sx={{fontSize: 12, height: 35}}>
              Extra Credit
            </Typography>
          </Stack>
          <Stack>
            <Typography color="text.primary" sx={{display: "inline-block", fontSize: 16, height: 35}}>
              {props.lecture.name}
            </Typography>
            <Typography color="text.primary" sx={{display: "inline-block", fontSize: 16, height: 35}}>
              {props.assignment.name}
              <Typography color="text.secondary" sx={{display: "inline-block", fontSize: 14, ml: 2, height: 35}}>
                {props.assignment.type}
              </Typography>
            </Typography>
            <Typography color="text.primary" sx={{display: "inline-block", fontSize: 16, height: 35}}>
              {gradeBook?.getPoints()}
              <Typography color="text.secondary" sx={{display: "inline-block", fontSize: 14, ml: 0.25}}>
                /{gradeBook?.getMaxPoints()}
              </Typography>
            </Typography>
            <Typography color="text.primary" sx={{display: "inline-block", fontSize: 16, height: 35}}>
              {gradeBook?.getExtraCredits()}
            </Typography>
          </Stack>
        </Stack>
      </Box>
      <Typography sx={{m: 2, mb: 0}}>
        Feedback Files
      </Typography>
      <FilesList path={path} sx={{m: 2}}/>
    </Box>
  )
}