import * as React from 'react';
import { Cell } from '@jupyterlab/cells';
import { Box, Divider, Grid, TextField, Typography } from '@mui/material';
import { CellModel, NbgraderData, ToolData } from '../../model';
import { GradeBook } from '../../../../services/gradebook';
import { Notebook } from '@jupyterlab/notebook';
import { IObservableJSON } from '@jupyterlab/observables';

export interface PointsComponentProps {
    metadata: IObservableJSON;
    gradebook: GradeBook;
    nbname: string;
    nbgraderData: NbgraderData;
    toolData: ToolData;

}

export const PointsComponent = (props: PointsComponentProps) => {
    const [points, setPoints] = React.useState(props.gradebook.getGradeScore(props.nbname,props.toolData.id));

    return (
        <Grid item>
            <TextField
                size='small'
                label="Points"
                type="number"
                value={points}
                onChange={(e) => {
                    setPoints(parseInt(e.target.value));    
                    props.metadata.set('updated',true);
                    props.gradebook.setManualScore(props.nbname, props.toolData.id, parseInt(e.target.value));
                }}
                InputProps={{
                    inputProps: {
                        max: props.toolData.points, min: 0
                    }
                }}
            />

        </Grid>
    );

}


export const ExtraCreditComponent = (props: PointsComponentProps) => {
    const [extraCredit, setExtraCredit] = React.useState(props.gradebook.getExtraCredit(props.nbname,props.toolData.id));

    return (
        <Grid item>
            <TextField
                size='small'
                label="Extra Credit"
                type="number"
                value={extraCredit}
                onChange={(e) => {
                    setExtraCredit(parseInt(e.target.value));
                    props.metadata.set('updated',true);
                    props.gradebook.setExtraCredit(props.nbname, props.toolData.id, parseInt(e.target.value));
                }}
                InputProps={{
                    inputProps: {
                        max: 10000, min: 0
                    }
                }}
            />
        </Grid>

    );

}