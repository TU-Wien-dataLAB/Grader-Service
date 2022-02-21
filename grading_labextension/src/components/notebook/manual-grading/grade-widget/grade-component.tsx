import * as React from 'react';
import { Cell } from '@jupyterlab/cells';
import { Box, Divider, Grid, TextField, Typography } from '@mui/material';
import { CellModel, NbgraderData, ToolData } from '../../model';
import { GradeBook } from '../../../../services/gradebook';
import { ExtraCreditComponent, PointsComponent } from './points-component';
import { CommentComponent } from './comment-component';


export interface GradeComponentProps {
    gradebook: GradeBook;
    nbname: string;
    nbgraderData: NbgraderData;
    toolData: ToolData;

}

export const GradeComponent = (props: GradeComponentProps) => {

    const gradableCell = (props.toolData.type !== "readonly" && props.toolData.type !== "solution" && props.toolData.type !== "");
    const showCommment = (props.toolData.type === "task" || props.toolData.type === "manual" || props.toolData.type === "solution");

    return (
        <Box>
            {(props.toolData.type !== "readonly" && props.toolData.type !== "") &&
                <Box sx={{ mt: 2, mb: 1, ml: 5 }}>
                    <Grid container spacing={2}>

                        {showCommment &&
                            <CommentComponent nbgraderData={props.nbgraderData} toolData={props.toolData} gradebook={props.gradebook} nbname={props.nbname}/>

                        }

                        {gradableCell &&
                            <PointsComponent nbgraderData={props.nbgraderData} toolData={props.toolData} gradebook={props.gradebook} nbname={props.nbname}/>
                        }

                        {gradableCell &&
                            <ExtraCreditComponent nbgraderData={props.nbgraderData} toolData={props.toolData} gradebook={props.gradebook} nbname={props.nbname}/>
                        }

                    </Grid>

                </Box>
            }
        </Box>
    );
}