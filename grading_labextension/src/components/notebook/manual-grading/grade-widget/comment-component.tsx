import * as React from 'react';
import { Cell } from '@jupyterlab/cells';
import { Box, Divider, Grid, TextField, Typography } from '@mui/material';
import { CellModel, NbgraderData, ToolData } from '../../model';
import { GradeBook } from '../../../../services/gradebook';

export interface CommentComponentProps {
    gradebook: GradeBook;
    nbname: string;
    nbgraderData: NbgraderData;
    toolData: ToolData;

}

export const CommentComponent = (props: CommentComponentProps) => {
    const [comment, setComment] = React.useState("");


    return (
        <Grid item>
            <TextField label="Comment"
                size='small'
                value={comment}
                onChange={(e) => {
                    setComment(e.target.value);
                    props.gradebook.setComment(props.nbname, props.toolData.id, e.target.value);
                }} />
        </Grid>
    );

}