import {
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  CardHeader,
  CircularProgress,
  Collapse,
  createTheme,
  IconButton,
  styled,
  ThemeProvider
} from '@mui/material';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { getAllAssignments } from '../../services/assignments.service';
import { AssignmentComponent } from './assignment';

interface ILectureComponentProps {
  lecture: Lecture;
}

export const LectureComponent = (props: ILectureComponentProps) => {
  const [assignments, setAssignments] = React.useState(null);
  const [expanded, setExpanded] = React.useState(false);

  React.useEffect(() => {
    getAllAssignments(props.lecture.id).then(result => {
      setAssignments(result);
    });
  }, []);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  if (assignments === null) {
    return (
      <div>
        <Card>
          <CircularProgress />
        </Card>
      </div>
    );
  }
  return (
    <div>
      <Card elevation={4} className="lecture-card">
        <CardActionArea onClick={handleExpandClick}>
          <CardHeader title={props.lecture.name}></CardHeader>
        </CardActionArea>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            {assignments.map((el: Assignment) => (
              <AssignmentComponent assignment={el} />
            ))}
          </CardContent>
        </Collapse>
      </Card>
    </div>
  );
};
