import * as React from 'react';
import { Cell } from '@jupyterlab/cells';
import { Box, Divider, Grid, TextField, Typography } from '@mui/material';
import { CellModel } from '../model';
import { GradeBook } from '../../../services/gradebook';


export interface GradeComponentProps {
    cell: Cell;
    gradebook: GradeBook;
    nbname: string;

}

export const GradeComponent = (props: GradeComponentProps) => {
    const nbgraderData = CellModel.getNbgraderData(props.cell.model.metadata);
    const toolData = CellModel.newToolData(nbgraderData, props.cell.model.type);
    //TODO: Read Data out of properties
    const [comment, setComment] = React.useState("");
    const [points, setPoints] = React.useState(props.gradebook.getAutoGradeScore(props.nbname,toolData.id));
    const [extraCredit, setExtraCredit] = React.useState(0);

    const gradableCell = (toolData.type !== "readonly" && toolData.type !== "solution" && toolData.type !== "");
    const showCommment = (toolData.type === "task" || toolData.type === "manual" || toolData.type === "solution");

    return (
        <Box>
            {(toolData.type !== "readonly" && toolData.type !== "") &&
                <Box sx={{ mt: 2, mb: 1, ml: 5 }}>
                    <Grid container spacing={2}>

                        {showCommment &&
                            <Grid item>
                                <TextField label="Comment"  
                                size='small'
                                value={comment}
                                onChange={(e) =>  {
                                    setComment(e.target.value);
                                    props.gradebook.setComment(props.nbname,toolData.id,e.target.value);
                                    }} />
                            </Grid>
                        }

                        {gradableCell &&
                            <Grid item>
                                <TextField
                                    size='small'
                                    label="Points"
                                    type="number"
                                    value={points}
                                    onChange={(e) =>  {
                                        setPoints(parseInt(e.target.value));
                                        props.gradebook.setManualScore(props.nbname,toolData.id, parseInt(e.target.value));
                                        }}
                                    InputProps={{
                                        inputProps: {
                                            max: toolData.points, min: 0
                                        }
                                    }}
                                />

                            </Grid>
                        }

                        {gradableCell &&
                            <Grid item>
                                <TextField
                                    size='small'
                                    label="Extra Credit"
                                    type="number"
                                    value={extraCredit}
                                    onChange={(e) =>  {
                                        setExtraCredit(parseInt(e.target.value));
                                        props.gradebook.setExtraCredit(props.nbname,toolData.id, parseInt(e.target.value));
                                        }}
                                    InputProps={{
                                        inputProps: {
                                            max: 10000, min: 0
                                        }
                                    }}
                                />
                            </Grid>
                        }
                    </Grid>

                </Box>
            }
        </Box>
    );
}