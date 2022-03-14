import { Box, Typography } from '@mui/material';
import * as React from 'react';

export interface IModalTitle {
  title: string;
  children?: React.ReactNode;
}

export const ModalTitle = (props: IModalTitle) => {
  return (
    <Box sx={{m: 3, top: 3 }}>
      <Typography display="inline-block" variant="h4">{props.title}</Typography>
      {props.children}
    </Box>
  );
};
