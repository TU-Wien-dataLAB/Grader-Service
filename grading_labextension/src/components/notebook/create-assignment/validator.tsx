import { Notebook } from "@jupyterlab/notebook";
import { Button } from '@blueprintjs/core';
import { Cell } from '@jupyterlab/cells';
import * as React from "react";
import { NbgraderData } from "../model";
import { PanelLayout } from "@lumino/widgets";
import { CellWidget } from "./cellwidget";
import { CreationWidget } from "./creation-widget";
import { ErrorWidget } from "./error-widget";


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
                        layout.addWidget(new ErrorWidget(c))
                    } else {
                        ids.add(metadata.grade_id);

                    }

                    
                }
            }
            
        })

    }
    return (
            <Button className="nbgrader-validate-button" onClick={validateNotebook} icon="automatic-updates" outlined intent="success">Validate</Button>
    );
}