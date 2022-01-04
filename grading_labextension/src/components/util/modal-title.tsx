import { Box, Typography } from '@mui/material';
import * as React from 'react';

export interface IModalTitle {
  title: string;
}

export const ModalTitle = (props: IModalTitle) => {
  return (
    <Box sx={{ m: 3, top: 4 }}>
      <Typography variant="h4">{props.title}</Typography>
    </Box>
  );
};
