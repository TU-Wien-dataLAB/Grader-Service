import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  CardHeader,
  CircularProgress,
  Collapse,
  createTheme,
  IconButton,
  LinearProgress,
  styled,
  ThemeProvider,
  Typography
} from '@mui/material';
import * as React from 'react';
import { Assignment } from '../../model/assignment';
import { Lecture } from '../../model/lecture';
import { getAllAssignments } from '../../services/assignments.service';
import { AssignmentComponent } from './assignment';
import { CreateDialog, EditLectureDialog } from './dialog';

interface ILectureComponentProps {
  lecture: Lecture;
  root: HTMLElement;
}

export const LectureComponent = (props: ILectureComponentProps) => {
  const [assignments, setAssignments] = React.useState(null);
  const [expanded, setExpanded] = React.useState(false);

  React.useEffect(() => {
    getAllAssignments(props.lecture.id).then(response => {
      setAssignments(response);
    });
  }, []);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  if (assignments === null) {
    return (
      <div>
        <Card>
          <LinearProgress />
        </Card>
      </div>
    );
  }
  return (
    <div>
      <Card
        sx={{ backgroundColor: expanded ? '#fafafa' : 'background.paper' }}
        elevation={expanded ? 0 : 2}
        className="lecture-card"
      >
        <CardContent sx={{ mb: -1, display: 'flex' }}>
          <Typography variant={'h5'} sx={{ mr: 2 }}>
            {props.lecture.name}
          </Typography>
          <EditLectureDialog
            lecture={props.lecture}
            handleSubmit={() => {
              console.log('update lecture');
            }}
          />
        </CardContent>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
              {assignments.map((el: Assignment) => (
                <AssignmentComponent
                  lecture={props.lecture}
                  assignment={el}
                  root={props.root}
                />
              ))}
            </Box>
          </CardContent>
        </Collapse>
        <CardActions>
          <CreateDialog
            lecture={props.lecture}
            handleSubmit={() => {
              getAllAssignments(props.lecture.id).then(response => {
                setAssignments(response);
              });
            }}
          />
          <Button size="small" sx={{ ml: 'auto' }} onClick={handleExpandClick}>
            {(expanded ? 'Hide' : 'Show') + ' Assignments'}
          </Button>
        </CardActions>
      </Card>
    </div>
  );
};
