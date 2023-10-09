// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { closeSnackbar, SnackbarProvider } from 'notistack';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { getRoutes } from '../components/assignment/routes';
import { loadString } from '../services/storage.service';
import { Router } from '@remix-run/router';
import { DialogProvider } from '../components/util/dialog-provider';
import { Button } from '@mui/material';
import { GlobalObjects } from '../index';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

export class AssignmentManageView extends ReactWidget {
  /**
   * Construct a new assignment list widget
   */
  router: Router;
  theme: 'dark' | 'light';

  constructor(options: AssignmentManageView.IOptions = {}) {
    super();
    this.id = options.id;
    this.addClass('GradingWidget');

    const savedPath = loadString('assignment-manage-react-router-path');
    let path = '/';
    if (savedPath !== null && savedPath !== '') {
      console.log(`Restoring path: ${savedPath}`);
      path = savedPath;
    }
    this.router = createMemoryRouter(getRoutes(), { initialEntries: [path] });

    const themeManager = GlobalObjects.themeManager;
    this.theme = (themeManager.isLight(themeManager.theme)) ? 'light' : 'dark';

    themeManager.themeChanged.connect(() => {
      this.theme = (themeManager.isLight(themeManager.theme)) ? 'light' : 'dark';
    }, this);
  }

  render() {
    return (
      <ThemeProvider theme={createTheme({ palette: { mode: this.theme } })}>
        <CssBaseline />
        <SnackbarProvider maxSnack={3}
                          action={(snackbarId) => (
                            <Button variant='outlined' size='small' style={{ color: 'white', borderColor: 'white' }}
                                    onClick={() => closeSnackbar(snackbarId)}>
                              Dismiss
                            </Button>
                          )}>
          <DialogProvider>
            <RouterProvider router={this.router} />
          </DialogProvider>
        </SnackbarProvider>
      </ThemeProvider>
    );
  }
}

export namespace AssignmentManageView {
  /**
   * An options object for initializing a assignment list view widget.
   */
  export interface IOptions {
    /**
     * The widget/DOM id of the assignment list view.
     */
    id?: string;
  }
}
