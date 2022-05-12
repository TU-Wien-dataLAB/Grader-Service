// Copyright (c) 2022, TU Wien
// All rights reserved.
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

import { Card, CardHeader, CardContent, Box, Paper } from '@mui/material';
import * as React from 'react';
import 'chart.js/auto';
import { Pie } from 'react-chartjs-2';
import { Submission } from '../../../model/submission';
import { Lecture } from '../../../model/lecture';
import { Assignment } from '../../../model/assignment';

export interface IChartsProps {
  lecture: Lecture;
  assignment: Assignment;
  users: { students: string[]; tutors: string[]; instructors: string[] };
  allSubmissions: Submission[];
}

export const GradingChart = (props: IChartsProps) => {
  const generateGradingData = (submissions: Submission[]) => {
    const data = [0, 0, 0, 0];
    let grading = 0;
    let done = 0;
    let failed = 0;
    let not = 0;
    for (const sub of submissions) {
      if (sub.feedback_available) {
        done++;
      } else if (
        sub.auto_status === 'automatically_graded' ||
        sub.manual_status === 'manually_graded'
      ) {
        grading++;
      } else if (sub.auto_status === 'grading_failed') {
        failed++;
      } else {
        not++;
      }
    }
    data[0] = done;
    data[1] = grading;
    data[2] = failed;
    data[3] = not;
    console.log(data);
    return data;
  };

  const [gradingData, setGradingData] = React.useState(
    generateGradingData(props.allSubmissions)
  );

  const gradingDataProps = {
    labels: [
      'Feedback Published',
      'Being Graded',
      'Grading Failed',
      'Not Yet Graded'
    ],
    datasets: [
      {
        label: 'Grading status',
        data: gradingData,
        backgroundColor: [
          'rgba(71,157,13,0.25)',
          'rgba(255,86,0,0.25)',
          'rgba(153,102,255,0.25)',
          'rgba(194,0,0,0.25)'
        ],
        borderColor: [
          'rgb(71,157,13)',
          'rgb(255,86,0)',
          'rgb(153,102,255)',
          'rgb(194,0,0)'
        ],
        borderWidth: 1
      }
    ]
  };

  return (
        <Box sx={{ height: '200px', width: '350px' }}>
          <Pie data={gradingDataProps} />
        </Box>
  );
};

export const SubmittedChart = (props: IChartsProps) => {
  const generateSubmittedData = (submissions: Submission[]) => {
    const data = [0, 0];
    const uniqueUsers = new Set<string>();
    submissions.forEach(s => uniqueUsers.add(s.username));
    data[0] =
      props.users.students.length +
      props.users.instructors.length +
      props.users.tutors.length -
      uniqueUsers.size;
    data[1] = uniqueUsers.size;
    return data;
  };

  const [submittedData, setSubmittedData] = React.useState(
    generateSubmittedData(props.allSubmissions)
  );

  const submittedDataProps = {
    labels: ['Has not submitted yet', 'Submitted at least once'],
    datasets: [
      {
        label: 'User Submission Status',
        data: submittedData,
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
        borderWidth: 1
      }
    ]
  };

  return (
    <Box sx={{ height: '200px', width: '350px' }}>
      <Pie data={submittedDataProps} />
    </Box>
  );
};
