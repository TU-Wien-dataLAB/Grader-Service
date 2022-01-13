import { Card, CardHeader, CardContent, Box } from '@mui/material';
import * as React from 'react';
import 'chart.js/auto';
import { Pie } from 'react-chartjs-2';
import { Submission } from '../../../model/submission';
import { Lecture } from '../../../model/lecture';
import { Assignment } from '../../../model/assignment';
import { getAllSubmissions } from '../../../services/submissions.service';

export interface ChartsProps {
    lecture : Lecture;
    assignment : Assignment;
    users : {students: string[], tutors: string[], instructors: string[]};
    allSubmissions: any[];
}

export const GradingChart = (props : ChartsProps) => {

    const generateGradingData = (submissions: {user:string,submissions:Submission[]}[]) => {
        const data = [1,1,1,1];
        let auto = 0;
        let manual = 0;
        let failed = 0;
        let not = 0;
        for (let s of submissions) {
            for(let sub of s.submissions) {
                if(sub.auto_status == "automatically_graded") {
                    if(sub.manual_status == "manually_graded") {
                        manual++;
                    } else {
                        auto++;
                    }
                } else if (sub.auto_status == "grading_failed") {
                    failed++;
                } else {
                    not++;
                }
            }
        }
        data[0] = auto;
        data[1] = manual;
        data[2] = failed;
        data[3] = not;
        console.log(data);
        return data;
    }
    
    const [gradingData, setGradingData] = React.useState(generateGradingData(props.allSubmissions));


      const gradingDataProps = {
        labels: ['Only autograded submissions', 'Autograded and manualgraded submissions', 'grading failed','not graded'],
        datasets: [
          {
            label: 'Grading status',
            data: gradingData,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1,
          },
        ],
      };

     
    return ( 
    <Card elevation={3} className='flexbox-item'>
        <CardHeader title="Grading Status" />
        <CardContent>
            <Box sx={{height:'300px', width:'300px'}}>
            <Pie data={gradingDataProps}/>
            </Box>
            
        </CardContent>
    </Card>
    );
}

export const SubmittedChart = (props : ChartsProps) => {

    const generateSubmittedData = (submissions : any) => {
        const data = [0,0];
        data[0] = props.users.students.length+props.users.instructors.length+props.users.tutors.length;
        data[1] = submissions.length;
        return data;
        }
    
    const [submittedData, setSubmittedData] = React.useState(generateSubmittedData(props.allSubmissions));



    const submittedDataProps = {
        labels: ['Has not submitted yet', 'Submitted at least once'],
        datasets: [
          {
            label: 'User Submission Status',
            data: submittedData,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1,
          },
        ],
      };
     
    return ( 
    <Card elevation={3} className='flexbox-item'>
        <CardHeader title="User Submission Status" />
        <CardContent>
            <Box sx={{height:'300px', width:'300px'}}>
            <Pie data={submittedDataProps}/>
            </Box>
            
        </CardContent>
    </Card>
    );
}