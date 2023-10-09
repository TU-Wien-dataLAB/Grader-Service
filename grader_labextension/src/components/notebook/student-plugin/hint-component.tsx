import * as React from 'react';
import { Alert, Collapse, createTheme } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/system';
import { GlobalObjects } from '../../../index';

export interface IHintComponentProps {
  hint: string;
  show: boolean;
}

export const HintComponent = (props: IHintComponentProps) => {
  const theme = createTheme({
    palette: { mode: (GlobalObjects.themeManager.isLight(GlobalObjects.themeManager.theme)) ? 'light' : 'dark' }
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Collapse in={props.show}>
        <Alert sx={{ mt: 1, mb: 1 }} severity='info'>
          {props.hint}
        </Alert>
      </Collapse>
    </ThemeProvider>
  );
};
