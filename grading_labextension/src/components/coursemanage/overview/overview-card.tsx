import { Card, CardContent, CardHeader, Chip, Typography } from '@mui/material';
import * as React from 'react';
import { Assignment } from '../../../model/assignment';

export interface OverviewCardProps {
    assignment: Assignment;
    allSubmissions: any[];
}

export const OverviewCard = (props: OverviewCardProps) => {


    return (
        <Card elevation={3} className="flexbox-item">
            <CardHeader title="Overview"/>
            <CardContent>
                <Typography variant='body1'>Users that submitted the assignment: <Chip label={props.allSubmissions.length}/></Typography>
            </CardContent>

        </Card>
    );
}