import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';
import { INotebookTools } from '@jupyterlab/notebook';

import { GradingView } from './widgets/grading';

import { checkIcon } from '@jupyterlab/ui-components'

// import { requestAPI } from './handler';

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

    // Create a blank content widget inside of a MainAreaWidget
    const content = new GradingView();
    const widget = new MainAreaWidget({ content });
    widget.id = 'grading-jupyterlab';
    widget.title.label = 'Grading';
    widget.title.closable = true;

    // Add an application command
    const command: string = 'grading:open';
    app.commands.addCommand(command, {
      label: 'Grading',
      execute: () => {
        if (!widget.isAttached) {
          // Attach the widget to the main work area if it's not there
          app.shell.add(widget, 'main');
        }
        // Activate the widget
        app.shell.activateById(widget.id);
      },
      icon: checkIcon
    });
    
    // Add the command to the launcher
    launcher.add({
      command: command,
      category: 'Grading',
      rank: 0
    });

    // Add the command to the palette.
    // palette.addItem({ command, category: 'Tutorial' });

    // Add the command to the Sidebar.
    // TODO: add grading to sidebar like file viewer and plugins etc
  }
};

export default extension;
