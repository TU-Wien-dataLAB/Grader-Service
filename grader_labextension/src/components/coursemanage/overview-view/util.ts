import {GlobalObjects} from "../../../index";
import {MainAreaWidget} from "@jupyterlab/apputils";
import {ITerminal} from '@jupyterlab/terminal';
import {Terminal} from '@jupyterlab/services';

let terminalSession: Terminal.ITerminalConnection = null;

export const openTerminal = async (path: string, showAlert?: (severity: string, msg: string) => void) => {
  console.log('Opening terminal at: ' + path.replace(' ', '\\ '));
  let args = {};
  if (
    terminalSession !== null &&
    terminalSession.connectionStatus === 'connected'
  ) {
    args = {name: terminalSession.name};
  }
  const main = (await GlobalObjects.commands.execute(
    'terminal:open',
    args
  )) as MainAreaWidget<ITerminal.ITerminal>;

  if (main) {
    const terminal = main.content;
    terminalSession = terminal.session;
  }

  try {
    terminalSession.send({
      type: 'stdin',
      content: ['cd ' + path.replace(' ', '\\ ') + '\n']
    });
  } catch (e) {
    showAlert('error', 'Error Opening Terminal');
    main.dispose();
  }
};

export const openBrowser = async (path: string, showAlert?: (severity: string, msg: string) => void) => {
  GlobalObjects.commands
    .execute('filebrowser:go-to-path', {
      path
    })
    .catch(_ => {
      showAlert('error', 'Error showing in File Browser');
    });
};
