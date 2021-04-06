import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';
import { INotebookTools } from '@jupyterlab/notebook';

import { GradingView } from './widgets/grading';

import { checkIcon, editIcon } from '@jupyterlab/ui-components'
import { AssignmentList } from './widgets/assignment-list';
import { CommandRegistry } from '@lumino/commands'

// import { requestAPI } from './handler';

namespace AssignmentsCommandIDs {
  export const create = 'assignments:create';

  export const open = 'assignments:open';
}

namespace GradingCommandIDs {
  export const create = 'grading:create';

  export const open = 'grading:open';
}

export class GlobalObjects {
  static commands: CommandRegistry;
}


/**
 * Initialization data for the grading extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'grading:plugin',
  autoStart: true,
  requires: [ICommandPalette, ILauncher, INotebookTools],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, launcher: ILauncher, nbtools: INotebookTools) => {
    console.log('JupyterLab extension grading is activated!');
    console.log('JupyterFrontEnd:', app)
    console.log('ICommandPalette:', palette);

    GlobalObjects.commands = app.commands;

    /* ##### Grading View Widget ##### */
    let command: string = GradingCommandIDs.create; 
    app.commands.addCommand(command, {
      execute: () => {
        // Create a blank content widget inside of a MainAreaWidget
        const gradingView = new GradingView();
        const gradingWidget = new MainAreaWidget<GradingView>({ content: gradingView });
        gradingWidget.id = 'grading-jupyterlab';
        gradingWidget.title.label = 'Grading';
        gradingWidget.title.closable = true;

        return gradingWidget;
      }
    })

    command = GradingCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Grading',
      execute: async () => {
        const gradingWidget = await app.commands.execute(GradingCommandIDs.create)

        if (!gradingWidget.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(gradingWidget, 'main');
        }
        // Activate the widget
        app.shell.activateById(gradingWidget.id);
      },
      icon: checkIcon
    });
    
    // Add the command to the launcher
    console.log("Add grading launcher");
    launcher.add({
      command: command,
      category: 'Assignments',
      rank: 0
    });



    // Add the command to the palette.
    // palette.addItem({ command, category: 'Tutorial' });

    // Add the command to the Sidebar.
    // TODO: add grading to sidebar like file viewer and plugins etc

    /* ##### Assignment List Widget ##### */

    command = AssignmentsCommandIDs.create;
    app.commands.addCommand(command, {
      execute: () => {
        // Create a blank content widget inside of a MainAreaWidget
        const assignmentList = new AssignmentList();
        const assignmentWidget = new MainAreaWidget<AssignmentList>({ content: assignmentList });
        assignmentWidget.id = 'assignments-jupyterlab';
        assignmentWidget.title.label = 'Assignments';
        assignmentWidget.title.closable = true;

        return assignmentWidget;
      }
    })

    command = AssignmentsCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Assignments',
      execute: async () => {
        const assignmentWidget: MainAreaWidget<AssignmentList> = await app.commands.execute(AssignmentsCommandIDs.create);

        if (!assignmentWidget.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(assignmentWidget, 'main');
        }
        // Activate the widget
        app.shell.activateById(assignmentWidget.id);
      },
      icon: editIcon
    });
    
    // Add the command to the launcher
    console.log("Add assignment launcher");
    launcher.add({
      command: command,
      category: 'Assignments',
      rank: 0
    });
  }
};

export default extension;
