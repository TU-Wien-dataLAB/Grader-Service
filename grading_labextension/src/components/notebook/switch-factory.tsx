import React from "react";
import { Scope, UserPermissions } from "../../services/permission.service";
import { CreationModeSwitch } from "./create-assignment/creation-switch";
import { GradingModeSwitch } from "./manual-grading/grading-switch";
import { ImodeSwitchProps, SwitchComponent } from "./slider";



export class SwitchModeFactory {
    public static getSwitch(props : ImodeSwitchProps) : JSX.Element {

        const paths = props.notebookpanel.context.contentsModel.path.split("/");
        const path = paths[0];
        const permissions = UserPermissions.getPermissions();
        const lecturecode = paths[1];
        let hasPermission = false;
        if (permissions.hasOwnProperty(lecturecode)) {
          hasPermission = permissions[lecturecode] !== Scope.student;
        }
        
        if(!hasPermission) {
          return null;
        }

        switch(path) {
            case 'source': return (
                <GradingModeSwitch
                  notebook={props.notebook}
                  notebookpanel={props.notebookpanel}
                  mode={props.mode}
                  onChange={props.onChange}
                />
              );
            case 'manualgrade': return (
                <CreationModeSwitch
                  notebook={props.notebook}
                  notebookpanel={props.notebookpanel}
                  mode={props.mode}
                  onChange={props.onChange}
                />
              );
            default: return null;
        }
    };
}