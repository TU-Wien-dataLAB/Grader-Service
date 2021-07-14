import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';
import { INotebookTools } from '@jupyterlab/notebook';

import { CourseManageView } from './widgets/coursemanage';

import { checkIcon, editIcon } from '@jupyterlab/ui-components'
import { AssignmentList } from './widgets/assignment-list';
import { CommandRegistry } from '@lumino/commands'
import { GradingView } from './widgets/grading';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ServiceManager } from '@jupyterlab/services';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';


namespace AssignmentsCommandIDs {
  export const create = 'assignments:create';

  export const open = 'assignments:open';
}

namespace CourseManageCommandIDs {
  export const create = 'coursemanage:create';

  export const open = 'coursemanage:open';
}

namespace GradingCommandIDs {
  export const create = 'grading:create';

  export const open = 'grading:open';
}

export class GlobalObjects {
  static commands: CommandRegistry;
  static docRegistry: DocumentRegistry;
  static serviceManager: ServiceManager;
  static docManager: IDocumentManager;
  static browserFactory: IFileBrowserFactory
}


/**
 * Initialization data for the grading extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'coursemanage:plugin',
  autoStart: true,
  requires: [ICommandPalette, ILauncher, INotebookTools, IDocumentManager, IFileBrowserFactory],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, launcher: ILauncher, nbtools: INotebookTools, docManager: IDocumentManager, browserFactory: IFileBrowserFactory,) => {
    console.log('JupyterLab extension grading is activated!');
    console.log('JupyterFrontEnd:', app)
    console.log('ICommandPalette:', palette);

    GlobalObjects.commands = app.commands;
    GlobalObjects.docRegistry = app.docRegistry;
    GlobalObjects.serviceManager = app.serviceManager;
    GlobalObjects.docManager = docManager;  
    GlobalObjects.browserFactory = browserFactory;
    
    /* ##### Course Manage View Widget ##### */
    let command: string = CourseManageCommandIDs.create;

    app.commands.addCommand(command, {
      execute: () => {
        // Create a blank content widget inside of a MainAreaWidget
        const gradingView = new CourseManageView();
        const gradingWidget = new MainAreaWidget<CourseManageView>({ content: gradingView });
        gradingWidget.id = 'coursemanage-jupyterlab';
        gradingWidget.title.label = 'Course Management';
        gradingWidget.title.closable = true;

        return gradingWidget;
      }
    })

    command = CourseManageCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Course Management',
      execute: async () => {
        const gradingWidget = await app.commands.execute(CourseManageCommandIDs.create)

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
    console.log("Add course management launcher");
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

    command = GradingCommandIDs.create;
    app.commands.addCommand(command, {
      execute: (args: any) => {
        const lectureID: number = typeof args['lectureID'] === 'undefined' ? null : (args['lectureID'] as number);
        const assignmentID: number = typeof args['assignmentID'] === 'undefined' ? null : (args['assignmentID'] as number);

        const gradingView = new GradingView({ lectureID, assignmentID });
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
      execute: async (args: any) => {
        const gradingView: MainAreaWidget<GradingView> = await app.commands.execute(GradingCommandIDs.create, args);

        if (!gradingView.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(gradingView, 'main');
        }
        // Activate the widget
        app.shell.activateById(gradingView.id);
      },
      icon: editIcon
    })

  }
};

export default extension;
