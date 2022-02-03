import * as React from 'react';
import { Cell, ICellModel } from '@jupyterlab/cells';
import { CellModel, CellType, NbgraderData, ToolData } from '../model';
import { Alert, Box, Divider, Grid, InputLabel, MenuItem, Select, SxProps, TextField } from '@mui/material';
import { CellTypeSwitcher } from '@jupyterlab/notebook';


export interface CreationComponentProps {
    cell: Cell;
}

const randomString = (length: number) => {
    let result = '';
    let chars = 'abcdef0123456789';
    let i;
    for (i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  }

export const CreationComponent = (props: CreationComponentProps) => {
    const nbgraderData = CellModel.getNbgraderData(props.cell.model.metadata);
    const toolData = CellModel.newToolData(nbgraderData, props.cell.model.type);
    const [type, setType] = React.useState(toolData.type);
    const [id, setId] = React.useState(toolData.id);

    const [points, setPoints] = React.useState(toolData.points);

    const updateMetadata = () => {
        toolData.type = type as CellType;
        if(id === "" || id === undefined) {
            toolData.id = "cell- "+randomString(16);
        } else {
            toolData.id = id;
        }
        toolData.points = points;
        const data = CellModel.newNbgraderData(toolData);
        CellModel.setNbgraderData(data, props.cell.model.metadata);
    }

  

    React.useEffect(() => {
        updateMetadata();
    })

    //TODO: should be done with mui themes
    const alertStyle = { width: 250 };
    const gradableCell = (type !== "readonly" as CellType && type !== "solution" as CellType && type !== "");

    return (
        <Box>
            <Divider />
            <Box sx={{ mt: 2, mb: 1, ml: 3 }}>
                <Box sx={{ mb: 1 }}>
                    <Grid container spacing={1}>
                        {/*<Grid item>
                            <Alert sx={alertStyle} variant='outlined' severity='error'>
                                Duplicate Id
                            </Alert>
                        </Grid> */}

                        {(points === undefined && gradableCell) &&
                            <Grid item>
                                <Alert variant='outlined' sx={alertStyle} severity='error'>
                                    Points not set
                                </Alert>
                            </Grid>
                        }

                        {type === "" &&
                            <Grid item>
                                <Alert variant='outlined' sx={alertStyle} severity='warning'>
                                    Type not set
                                </Alert>
                            </Grid>
                        }

                        {points == 0 &&
                            <Grid item>
                                <Alert variant='outlined' sx={alertStyle} severity='error'>
                                    Gradable cell with zero points
                                </Alert>
                            </Grid>
                        }
                    </Grid>
                </Box>

                <Grid container spacing={1}>
                    <Grid item>
                        <TextField label="Type" select size='small' sx={{ minWidth: 150 }} value={type} onChange={(e) => { setType(e.target.value as CellType) }}>
                            <MenuItem value=''>-</MenuItem>
                            <MenuItem value='readonly'>Readonly</MenuItem>
                            {props.cell.model.type == 'code' && <MenuItem value='solution'>Autograded answer</MenuItem>}
                            {props.cell.model.type == 'code' && <MenuItem value='tests'>Autograded tests</MenuItem>}

                            <MenuItem value='manual'>Manual graded answer</MenuItem>
                            <MenuItem value='task'>Manual graded task</MenuItem>
                        </TextField>
                    </Grid>

                    {type !== "" &&
                        <Grid item>
                            <TextField
                                size='small'
                                label="ID"
                                value={id}
                                onChange={(e) => setId(e.target.value)}>
                            </TextField>
                        </Grid>
                    }

                    {gradableCell &&
                        <Grid item>
                            <TextField
                                size='small'
                                label="Points"
                                value={points}
                                type="number"
                                onChange={(e) => setPoints(parseInt(e.target.value))}
                                InputProps={{
                                    inputProps: {
                                        max: 10000, min: 0
                                    }
                                }} />

                        </Grid>
                    }

                </Grid>
            </Box>
        </Box>
    )
}
