import {Lecture} from "../../../model/lecture";
import {Assignment} from "../../../model/assignment";
import {Box, Card, CardContent, CardHeader, Typography} from "@mui/material";
import Timeline from '@mui/lab/Timeline';
import TimelineItem from '@mui/lab/TimelineItem';
import TimelineSeparator from '@mui/lab/TimelineSeparator';
import TimelineConnector from '@mui/lab/TimelineConnector';
import TimelineContent from '@mui/lab/TimelineContent';
import TimelineDot from '@mui/lab/TimelineDot';

import * as React from "react";
import {getGitLog, IGitLogObject} from "../../../services/file.service";
import {utcToLocalFormat} from "../../../services/datetime.service";
import {TimelineOppositeContent} from "@mui/lab";
import { RepoType } from "../../util/repo-type";

interface IGitLogProps {
  lecture: Lecture;
  assignment: Assignment;
  repoType: RepoType;
}

const getTimelineItem = (logItem: IGitLogObject) => {
  let date = utcToLocalFormat(logItem.date).split(" ", 2);
  return <TimelineItem className={"git-timeline-item"}>
    <TimelineOppositeContent>
      <Typography sx={{fontSize: 14, mt: 0.25}}>
        {date[1]}
      </Typography>
      <Typography color="text.secondary" sx={{fontSize: 11}}>
        {date[0]}
      </Typography>
    </TimelineOppositeContent>
    <TimelineSeparator>
      <TimelineDot color="primary"/>
      <TimelineConnector/>
    </TimelineSeparator>
    <TimelineContent>
      <Typography sx={{fontSize: 16, fontWeight: 'fontWeightMedium'}}>
        {logItem.commit.substring(0, 7)}
        <Typography sx={{fontSize: 10, ml: 1, display: "inline-block"}}>
          {logItem.ref.replace("->", "→")}
        </Typography>
      </Typography>
      <Typography>
        <Typography color="text.secondary" sx={{fontSize: 13, display: "inline-block"}}>
          {logItem.author}
        </Typography>
      </Typography>
    </TimelineContent>
  </TimelineItem>
}

export const GitLog = (props: IGitLogProps) => {
  const [gitLogs, setGitLogs] = React.useState([] as IGitLogObject[]);
  React.useEffect(() => {
    getGitLog(props.lecture, props.assignment, props.repoType, 10).then(logs => setGitLogs(logs))
  }, [props])

  return (
    <Card elevation={3} className='flexbox-item'>
      <CardHeader title="Git Log"/>
      <CardContent sx={{height: '300px', width: '300px', overflowY: "auto"}}>
        <Timeline sx={{m: 0, p: 0, ml: -2}}>
          {gitLogs.map(log => getTimelineItem(log))}
        </Timeline>
      </CardContent>
    </Card>
  );
}