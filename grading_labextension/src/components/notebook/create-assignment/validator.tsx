import { Notebook } from "@jupyterlab/notebook";
import { Button, ButtonProps } from "@mui/material";
import { Cell } from '@jupyterlab/cells';
import * as React from "react";
import { NbgraderData } from "../model";
import { PanelLayout } from "@lumino/widgets";
import { CellWidget } from "./cellwidget";
import { purple } from '@mui/material/colors';
import { styled } from '@mui/material/styles';


export interface ValidatorProps {
    notebook: Notebook;
}



export const Validator = (props : ValidatorProps) => {
    const validateNotebook = () => {
        //check duplicate ids
        const ids = new Set()
        const errors = []
        console.log("started validation");
        props.notebook.widgets.map((c : Cell) => {
            const metadata : NbgraderData = c.model.metadata.get("nbgrader").valueOf() as NbgraderData;
            if(metadata !== null) {
                if(metadata.grade_id !== null) {
                    if(ids.has(metadata.grade_id)) {
                        console.log("duplicate id found");
                        const layout = c.layout as PanelLayout;
                    const widget = layout.widgets[0] as CellWidget;
                    } else {
                        ids.add(metadata.grade_id);

                    }

                    
                }
            }
            
        })

    }
    return (
        <button className=".MuiButton-textSizeSmall" onClick={validateNotebook}>Validate</button>
    );
}