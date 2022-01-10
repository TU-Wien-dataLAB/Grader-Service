import { Box, Typography } from '@mui/material';
import * as React from 'react';

export interface IModalTitle {
  title: string;
  children?: React.ReactNode;
}

export const ModalTitle = (props: IModalTitle) => {
  return (
    <Box sx={{position:'absolute', m: 3, top: 4 }}>
      <Typography display="inline-block" variant="h4">{props.title}</Typography>
      {props.children}
    </Box>
  );
};
