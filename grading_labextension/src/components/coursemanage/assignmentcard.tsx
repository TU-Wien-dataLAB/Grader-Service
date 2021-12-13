import { AppBar, Button, Card, CardActionArea, CardContent, CardHeader, Dialog, Divider, IconButton, List, ListItem, ListItemText, Paper, Slide, Toolbar, Typography } from "@mui/material";
import React from "react";
import CloseIcon from '@mui/icons-material/Close';
import { TransitionProps } from '@mui/material/transitions';
import { Assignment } from "../../model/assignment";


const Transition = React.forwardRef(function Transition(
  props: TransitionProps & {
    children: React.ReactElement;
  },
  ref: React.Ref<unknown>,
) {
  return <Slide direction="up" ref={ref} {...props} />;
});

export const AssignmentCard = (a: any) => {
  const [open, setOpen] = React.useState(false);
  const [assignment, setAssignment] = React.useState(a.assignment);

  return (
    <div>
      <Card >
      <CardActionArea onClick={() => setOpen(true)}>
        <CardContent>
          
            <Typography gutterBottom variant="h5" component="div">
              {assignment.name}
            </Typography>
          
        </CardContent>
        </CardActionArea>
      </Card>

      <Dialog
        fullScreen
        open={open}
        onClose={() => setOpen(false)}
        TransitionComponent={Transition}
      >
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={() => setOpen(false)}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              {assignment.name}
            </Typography>
          </Toolbar>
        </AppBar>
        <Paper>
          yo
        </Paper>
      </Dialog>
    </div>

  );
}