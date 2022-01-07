import { Card, CardHeader, CardContent, Box } from '@mui/material';
import * as React from 'react';
import 'chart.js/auto';
import { Pie } from 'react-chartjs-2';
import { Submission } from '../../model/submission';
import { Lecture } from '../../model/lecture';
import { Assignment } from '../../model/assignment';
import { getAllSubmissions } from '../../services/submissions.service';

export interface ChartProps {
    lecture : Lecture;
    assignment : Assignment;
    allSubmissions: any[];
}

export const Charts = (props : ChartProps) => {

    const generateSubmittedData = (submissions : any) => {
        const data = [1,0,0];
        //TODO: set data of users that have not submitted yet 


        let i: number, j: number = 0;
        submissions.forEach((e: { submissions: any[]; }) => {
            if(e.submissions.length == 1) {
                i++;
            } else {
                j++;
            }
        });
        data[1] = i;
        data[2] = j;
        
        return data;
        }

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
    
    const [submittedData, setSubmittedData] = React.useState(generateSubmittedData(props.allSubmissions));
    const [gradingData, setGradingData] = React.useState(generateGradingData(props.allSubmissions));



    const submittedDataProps = {
        labels: ['Has not submitted yet', 'Submitted at least once', 'Submitted more than once'],
        datasets: [
          {
            label: 'User Submission Status',
            data: submittedData,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(75, 192, 192, 0.2)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(75, 192, 192, 1)',
            ],
            borderWidth: 1,
          },
        ],
      };

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
    <Card elevation={3}>
        <CardHeader title="Charts" />
        <CardContent>
            <Box sx={{height:'300px', width:'300px'}}>
            <Pie data={submittedDataProps}/>
            </Box>
            <Box sx={{height:'300px', width:'300px'}}>
            <Pie data={gradingDataProps}/>
            </Box>
            
        </CardContent>
    </Card>);
}