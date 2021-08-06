import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';
import { INotebookTools } from '@jupyterlab/notebook';

import { CourseManageView } from './widgets/coursemanage';

import {
  INotebookTracker
} from '@jupyterlab/notebook';

import {
  BoxPanel
} from '@lumino/widgets';

import {
  CreateAssignmentWidget
} from './create-assignment/extension';

import { checkIcon, editIcon } from '@jupyterlab/ui-components'
import { AssignmentList } from './widgets/assignment-list';
import { CommandRegistry } from '@lumino/commands'
import { GradingView } from './widgets/grading';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ServiceManager } from '@jupyterlab/services';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { UserPermissions } from './services/permission.service';


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

namespace CreateAssignmentIDs {
  export const create = 'create-assignment:create';
  
  export const open = 'create-assignment:open';
}

export class GlobalObjects {
  static commands: CommandRegistry;
  static docRegistry: DocumentRegistry;
  static serviceManager: ServiceManager;
  static docManager: IDocumentManager;
  static browserFactory: IFileBrowserFactory;
  static tracker: INotebookTracker;
}


/**
 * Initialization data for the grading extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'coursemanage:plugin',
  autoStart: true,
  requires: [ICommandPalette, ILauncher, INotebookTools, IDocumentManager, IFileBrowserFactory, INotebookTracker],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette, launcher: ILauncher, nbtools: INotebookTools, docManager: IDocumentManager, browserFactory: IFileBrowserFactory, tracker: INotebookTracker) => {
    console.log('JupyterLab extension grading is activated!');
    console.log('JupyterFrontEnd:', app)
    console.log('ICommandPalette:', palette);
    console.log('Tracker', tracker)

    GlobalObjects.commands = app.commands;
    GlobalObjects.docRegistry = app.docRegistry;
    GlobalObjects.serviceManager = app.serviceManager;
    GlobalObjects.docManager = docManager;
    GlobalObjects.browserFactory = browserFactory;
    GlobalObjects.tracker = tracker;

    console.log('Activating extension "create_assignment".');
    const panel = new BoxPanel();
    const createAssignmentWidget = new CreateAssignmentWidget(tracker);
    panel.addWidget(createAssignmentWidget);
    panel.id = 'nbgrader-create_assignemnt';
    panel.title.label = 'Create Assignment';
    panel.title.caption = 'nbgrader Create Assignment';
    app.shell.add(panel, 'right');
    console.log('Extension "create_assignment" activated.');

    let command : string = CreateAssignmentIDs.open;
    app.commands.addCommand(command, {
      label: 'Create Assignment',
      execute: async () => {

       
      },
      icon: editIcon
    });

    /* ##### Course Manage View Widget ##### */
    command = CourseManageCommandIDs.create;

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

    // If the user has no instructor roles in any lecture we do not display the course management
    UserPermissions.loadPermissions().then(() => {
      let permissions = UserPermissions.getPermissions()
      let sum = 0;
      for (var el in permissions) {
        if (permissions.hasOwnProperty(el)) {
          sum += permissions[el];
        }
      }
      if (sum != 0) {
        console.log("Non-student permissions found! Adding coursemanage launcher");
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
      }
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
