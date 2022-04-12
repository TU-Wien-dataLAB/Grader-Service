import { Box, IconButton, Menu, MenuItem } from '@mui/material';
import * as React from 'react';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { PageConfig } from '@jupyterlab/coreutils';
import { GlobalObjects } from '../../../index';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { ITerminal } from '@jupyterlab/terminal';
import { Terminal } from '@jupyterlab/services';
import { Assignment } from '../../../model/assignment';
import { Lecture } from '../../../model/lecture';

export interface ISettingsProps {
  lecture: Lecture;
  assignment: Assignment;
  selectedDir: string;
}

export const Settings = (props: ISettingsProps) => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const serverRoot = PageConfig.getOption('serverRoot');
  let terminalSession: Terminal.ITerminalConnection = null;

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const openTerminal = async () => {
    const path = `${serverRoot}/${props.selectedDir}/${props.lecture.code}/${props.assignment.name}`;
    console.log('Opening terminal at: ' + path.replace(' ', '\\ '));
    let args = {};
    if (
      terminalSession !== null &&
      terminalSession.connectionStatus === 'connected'
    ) {
      args = { name: terminalSession.name };
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
      //showAlert('error', 'Error Opening Terminal');
      main.dispose();
    }
    handleClose();
  };

  const openBrowser = async () => {
    const path = `${props.selectedDir}/${props.lecture.code}/${props.assignment.name}`;
    GlobalObjects.commands
      .execute('filebrowser:go-to-path', {
        path
      })
      .catch(error => {
        //showAlert('error', 'Error showing in File Browser');
      });
    handleClose();
  };

  return (
    <Box>
      <IconButton
        aria-label="settings"
        aria-controls={open ? 'basic-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
      >
        <MoreVertIcon />
      </IconButton>

      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button'
        }}
      >
        <MenuItem onClick={openBrowser}>Show Files in Filebrowser</MenuItem>
        <MenuItem onClick={openTerminal}>Open Terminal</MenuItem>
      </Menu>
    </Box>
  );
};
