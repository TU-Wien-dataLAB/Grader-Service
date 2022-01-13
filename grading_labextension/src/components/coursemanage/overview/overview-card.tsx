import { Card, CardContent, CardHeader, Chip, Typography } from '@mui/material';
import * as React from 'react';
import { Assignment } from '../../../model/assignment';

export interface OverviewCardProps {
    assignment: Assignment;
    allSubmissions: any[];
    users : {students: string[], tutors: string[], instructors: string[]};
}

export const OverviewCard = (props: OverviewCardProps) => {


    return (
        <Card elevation={3} className="flexbox-item">
            <CardHeader title="Overview"/>
            <CardContent sx={{alignItems:{xs: 'center'}}}>
                <Typography variant='body1'>Students: 
                    <Chip color={'primary'} variant='outlined' label={props.users.students.length}/>
                </Typography>

                <Typography variant='body1'>Tutors: 
                    <Chip color={'primary'} variant='outlined' label={props.users.tutors.length}/>
                </Typography>

                <Typography variant='body1'>Instructors: 
                    <Chip color={'primary'} variant='outlined' label={props.users.instructors.length}/>
                </Typography>

                <Typography variant='body1'>Users that submitted the assignment: 
                    <Chip color={'primary'} variant='outlined' label={props.allSubmissions.length}/>
                </Typography>

            </CardContent>

        </Card>
    );
}