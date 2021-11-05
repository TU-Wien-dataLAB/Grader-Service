/* eslint-disable no-constant-condition */
/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-prototype-builtins */
import {
  ILayoutRestorer,
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget, WidgetTracker, IWidgetTracker } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';
import { INotebookTools, Notebook, NotebookPanel } from '@jupyterlab/notebook';

import { CourseManageView } from './widgets/coursemanage';

import { Cell } from '@jupyterlab/cells';

import { INotebookTracker } from '@jupyterlab/notebook';

import { CellWidget } from './components/create-assignment/cellwidget';

import { PanelLayout } from '@lumino/widgets';

import { CreationmodeSwitch } from './components/create-assignment/slider';

import { checkIcon, editIcon } from '@jupyterlab/ui-components';
import { AssignmentList } from './widgets/assignment-list';
import { CommandRegistry } from '@lumino/commands';
import { GradingView } from './widgets/grading';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { ServiceManager } from '@jupyterlab/services';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { UserPermissions } from './services/permission.service';
import { CellPlayButton } from './components/create-assignment/widget';
import { ManualGradingView } from './widgets/manualgrading';
import { FeedbackView } from './widgets/feedback';

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

namespace ManualGradeCommandIDs {
  export const create = 'manualgrade:create';

  export const open = 'manualgrade:open'
}

namespace FeedbackCommandIDs {
  export const create = 'feedback:create';

  export const open = 'feedback:open'
}

/*namespace CreateAssignmentIDs {
  export const create = 'create-assignment:create';
  
  export const open = 'create-assignment:open';
}*/

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
  requires: [
    ICommandPalette,
    ILauncher,
    INotebookTools,
    IDocumentManager,
    IFileBrowserFactory,
    INotebookTracker,
    ILayoutRestorer
  ],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    launcher: ILauncher,
    nbtools: INotebookTools,
    docManager: IDocumentManager,
    browserFactory: IFileBrowserFactory,
    tracker: INotebookTracker,
    restorer: ILayoutRestorer
  ) => {
    console.log('JupyterLab extension grading is activated!');
    console.log('JupyterFrontEnd:', app);
    console.log('ICommandPalette:', palette);
    console.log('Tracker', tracker);

    GlobalObjects.commands = app.commands;
    GlobalObjects.docRegistry = app.docRegistry;
    GlobalObjects.serviceManager = app.serviceManager;
    GlobalObjects.docManager = docManager;
    GlobalObjects.browserFactory = browserFactory;
    GlobalObjects.tracker = tracker;

    const assignmentTracker = new WidgetTracker<MainAreaWidget<AssignmentList>>({
      namespace: 'grader-assignments',
    });

    restorer.restore(assignmentTracker, {
      command: AssignmentsCommandIDs.open,
      name: () => 'grader-assignments',
    });

    const courseManageTracker = new WidgetTracker<MainAreaWidget<CourseManageView>>({
      namespace: 'grader-coursemanage',
    });

    restorer.restore(courseManageTracker, {
      command: CourseManageCommandIDs.open,
      name: () => 'grader-coursemanage',
    });

    const manualGradingTracker = new WidgetTracker<MainAreaWidget<ManualGradingView>>({
      namespace: 'grader-manual-grading',
    });

    restorer.restore(manualGradingTracker, {
      command: ManualGradeCommandIDs.open,
      args: (widget) => ({ 
        lectureID: widget.content.lectureID, 
        assignmentID: widget.content.assignmentID,
        subID: widget.content.subID,
        username: widget.content.username 
      }),
      name: () => 'grader-manual-grading',
    });

    //Creation of in-cell widget for create assignment
    let connectTrackerSignals = (tracker: INotebookTracker) => {
      tracker.currentChanged.connect(async () => {
        const notebookPanel = tracker.currentWidget;
        const notebook: Notebook = tracker.currentWidget.content;
        const creationmode = false;

        notebookPanel.context.ready.then(() => {
          //Creation of widget switch
          const switcher: CreationmodeSwitch = new CreationmodeSwitch(
            creationmode,
            notebookPanel,
            notebook
          );
          notebookPanel.toolbar.insertItem(10, 'Creationmode', switcher);
        });
      }, this);

      tracker.activeCellChanged.connect(() => {
        const notebookPanel: NotebookPanel = tracker.currentWidget;
        const notebook: Notebook = tracker.currentWidget.content;
        const notebookPaths: string[] = notebookPanel.context.contentsModel.path.split("/")
        if (notebookPaths[0] == "manualgrade") return;
        const switcher: any = (notebookPanel.toolbar.layout as PanelLayout)
          .widgets[10]; // TODO: instead of indexing use search for instance of CreationmodeSwitch; maybe other plugins change index
        // Remove the existing play button from
        // the previously active cell. This may
        // well introduce bugs down the road and
        // there is likely a better way to do this
        notebook.widgets.map((c: Cell) => {
          const currentLayout = c.layout as PanelLayout;
          currentLayout.widgets.map(w => {
            if (w instanceof CellPlayButton) {
              currentLayout.removeWidget(w);
            }
          });
        });

        const cell: Cell = notebook.activeCell;
        const newButton: CellPlayButton = new CellPlayButton(
          cell,
          notebookPanel.sessionContext,
          switcher.mode
        );
        (cell.layout as PanelLayout).insertWidget(2, newButton);
        //check if in creationmode and new cell was inserted
        if (
          switcher.mode &&
          (cell.layout as PanelLayout).widgets.every(w => {
            if (w instanceof CellWidget) {
              return false;
            }
            return true;
          })
        ) {
          (cell.layout as PanelLayout).insertWidget(0, new CellWidget(cell));
        }
      }, this);
    };

    /* ##### Course Manage View Widget ##### */
    let command: string = CourseManageCommandIDs.create;

    app.commands.addCommand(command, {
      execute: () => {
        // Create a blank content widget inside of a MainAreaWidget
        const gradingView = new CourseManageView();
        const gradingWidget = new MainAreaWidget<CourseManageView>({
          content: gradingView
        });
        gradingWidget.id = 'coursemanage-jupyterlab';
        gradingWidget.title.label = 'Course Management';
        gradingWidget.title.closable = true;

        courseManageTracker.add(gradingWidget);

        return gradingWidget;
      }
    });

    // If the user has no instructor roles in any lecture we do not display the course management
    UserPermissions.loadPermissions().then(() => {
      const permissions = UserPermissions.getPermissions();
      let sum = 0;
      for (const el in permissions) {
        if (permissions.hasOwnProperty(el)) {
          sum += permissions[el];
        }
      }
      if (sum !== 0) {
        console.log(
          'Non-student permissions found! Adding coursemanage launcher and connecting creation mode'
        );
        connectTrackerSignals(tracker);

        command = CourseManageCommandIDs.open;
        app.commands.addCommand(command, {
          label: 'Course Management',
          execute: async () => {
            const gradingWidget = await app.commands.execute(
              CourseManageCommandIDs.create
            );

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
        console.log('Add course management launcher');
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
        const assignmentWidget = new MainAreaWidget<AssignmentList>({
          content: assignmentList
        });
        assignmentWidget.id = 'assignments-jupyterlab';
        assignmentWidget.title.label = 'Assignments';
        assignmentWidget.title.closable = true;

        assignmentTracker.add(assignmentWidget);

        return assignmentWidget;
      }
    });

    command = AssignmentsCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Assignments',
      execute: async () => {
        const assignmentWidget: MainAreaWidget<AssignmentList> = await app.commands.execute(
          AssignmentsCommandIDs.create
        );

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
    console.log('Add assignment launcher');
    launcher.add({
      command: command,
      category: 'Assignments',
      rank: 0
    });

    command = GradingCommandIDs.create;
    app.commands.addCommand(command, {
      execute: (args: any) => {
        const lectureID: number =
          typeof args['lectureID'] === 'undefined'
            ? null
            : (args['lectureID'] as number);
        const assignmentID: number =
          typeof args['assignmentID'] === 'undefined'
            ? null
            : (args['assignmentID'] as number);

        const gradingView = new GradingView({ lectureID, assignmentID });
        const gradingWidget = new MainAreaWidget<GradingView>({
          content: gradingView
        });
        gradingWidget.id = 'grading-jupyterlab';
        gradingWidget.title.label = 'Grading';
        gradingWidget.title.closable = true;

        return gradingWidget;
      }
    });

    command = GradingCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Grading',
      execute: async (args: any) => {
        const gradingView: MainAreaWidget<GradingView> = await app.commands.execute(
          GradingCommandIDs.create,
          args
        );

        if (!gradingView.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(gradingView, 'main');
        }
        // Activate the widget
        app.shell.activateById(gradingView.id);
      },
      icon: editIcon
    });

    command = ManualGradeCommandIDs.create;
    app.commands.addCommand(command, {
      execute: (args: any) => {
        const lectureID: number =
          typeof args['lectureID'] === 'undefined'
            ? null
            : (args['lectureID'] as number);
        const assignmentID: number =
          typeof args['assignmentID'] === 'undefined'
            ? null
            : (args['assignmentID'] as number);
        const subID: number =
          typeof args['subID'] === 'undefined'
            ? null
            : (args['subID'] as number);
        const username: string =
          typeof args['username'] === 'undefined'
            ? null
            : (args['username'] as string);
        const manualgradingView = new ManualGradingView({ lectureID, assignmentID, subID, username });
        const manualgradingWidget = new MainAreaWidget<ManualGradingView>({
          content: manualgradingView
        });
        manualgradingWidget.id = 'manual-grading-jupyterlab';
        manualgradingWidget.title.label = 'Manualgrading';
        manualgradingWidget.title.closable = true;

        manualGradingTracker.add(manualgradingWidget);

        return manualgradingWidget;
      }
    });

    command = ManualGradeCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'ManualGrading',
      execute: async (args: any) => {
        const gradingView: MainAreaWidget<ManualGradingView> = await app.commands.execute(
          ManualGradeCommandIDs.create,
          args
        );

        if (!gradingView.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(gradingView, 'main');
        }
        // Activate the widget
        app.shell.activateById(gradingView.id);
      },
      icon: editIcon
    });

    command = FeedbackCommandIDs.create;
    app.commands.addCommand(command, {
      execute: (args: any) => {
        const lectureID: number =
          typeof args['lectureID'] === 'undefined'
            ? null
            : (args['lectureID'] as number);
        const assignmentID: number =
          typeof args['assignmentID'] === 'undefined'
            ? null
            : (args['assignmentID'] as number);
        const subID: number =
          typeof args['subID'] === 'undefined'
            ? null
            : (args['subID'] as number);
        const feedbackView = new FeedbackView({ lectureID, assignmentID, subID });
        const feedbackWidget = new MainAreaWidget<FeedbackView>({
          content: feedbackView
        });
        feedbackWidget.id = 'feedback-jupyterlab';
        feedbackWidget.title.label = 'Feedback';
        feedbackWidget.title.closable = true;

        return feedbackWidget;
      }
    });

    command = FeedbackCommandIDs.open;
    app.commands.addCommand(command, {
      label: 'Feedback',
      execute: async (args: any) => {
        const feedbackWidget: MainAreaWidget<FeedbackView> = await app.commands.execute(
          FeedbackCommandIDs.create,
          args
        );

        if (!feedbackWidget.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(feedbackWidget, 'main');
        }
        // Activate the widget
        app.shell.activateById(feedbackWidget.id);
      },
      icon: editIcon
    });
  }
};

export default extension;
