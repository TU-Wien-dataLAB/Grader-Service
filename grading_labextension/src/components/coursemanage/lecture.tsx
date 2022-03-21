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
import { getLecture, getUsers } from '../../services/lectures.service';

interface ILectureComponentProps {
  lecture: Lecture;
  root: HTMLElement;
  showAlert: (severity: string, msg: string) => void;
  expanded?: boolean;
}

export const LectureComponent = (props: ILectureComponentProps) => {
  const [lecture, setLecture] = React.useState(props.lecture);
  const [assignments, setAssignments] = React.useState(null);
  const [expanded, setExpanded] = React.useState(props.expanded === undefined ? false : props.expanded);
  const [users, setUsers] = React.useState(null);

  React.useEffect(() => {
    getAllAssignments(lecture.id).then(response => {
      setAssignments(response);
    });

    getUsers(lecture).then(response => { 
      setUsers(response) 
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
            {lecture.name}
          </Typography>
          <EditLectureDialog
            lecture={lecture}
            handleSubmit={async () => {
              setLecture(await getLecture(lecture.id));
            }}
          />
        </CardContent>

        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
              {assignments.map((el: Assignment) => (
                <AssignmentComponent
                  lecture={lecture}
                  assignment={el}
                  root={props.root}
                  users={users}
                  showAlert={props.showAlert}
                />
              ))}
            </Box>
          </CardContent>
        </Collapse>
        <CardActions>
          <CreateDialog
            lecture={lecture}
            handleSubmit={() => {
              getAllAssignments(lecture.id).then(response => {
                setAssignments(response);
              });
              setExpanded(true);
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
