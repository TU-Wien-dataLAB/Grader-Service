import * as React from 'react';
import moment from 'moment';
import { Chip } from '@mui/material';
import AccessAlarmRoundedIcon from '@mui/icons-material/AccessAlarmRounded';
import { SxProps } from '@mui/system';
import { Theme } from '@mui/material/styles';

export interface IDeadlineProps {
  due_date: string | null;
  compact: boolean;
  sx?: SxProps<Theme>;
}

interface ITimeSpec {
  weeks: number;
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
}

interface IUnitMap {
  [name: string]: string;
}
const compactTimeUnits: IUnitMap = {
  w: 'W',
  d: 'd',
  h: 'h',
  m: 'm',
  s: 's'
};

const fullTimeUnits: IUnitMap = {
  w: 'Week',
  d: 'Day',
  h: 'Hour',
  m: 'Minute',
  s: 'Second'
};

const getTimeUnit = (timeUnit: string, value: number, compact: boolean) => {
  if (compact) {
    return `${value}${compactTimeUnits[timeUnit]}`;
  }
  if (value === 1) {
    return `${value} ${fullTimeUnits[timeUnit]}`;
  } else {
    return `${value} ${fullTimeUnits[timeUnit]}s`;
  }
};

const calculateTimeLeft = (date: Date) => {
  const difference = +date - +new Date();
  const timeLeft: ITimeSpec = {
    weeks: Math.floor(difference / (1000 * 60 * 60 * 24 * 7)),
    days: Math.floor((difference / (1000 * 60 * 60 * 24)) % 7),
    hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
    minutes: Math.floor((difference / 1000 / 60) % 60),
    seconds: Math.floor((difference / 1000) % 60)
  };
  return timeLeft;
};

function getDisplayDate(date: Date, compact: boolean): string {
  const time: ITimeSpec = calculateTimeLeft(date);
  if (time.weeks === 0) {
    if (time.days === 0) {
      return `${getTimeUnit('h', time.hours, compact)} ${getTimeUnit(
        'm',
        time.minutes,
        compact
      )} ${getTimeUnit('s', time.seconds, compact)}`;
    } else {
      return `${getTimeUnit('d', time.days, compact)} ${getTimeUnit(
        'h',
        time.hours,
        compact
      )} ${getTimeUnit('m', time.minutes, compact)}`;
    }
  } else if (time.weeks > 0) {
    return `${getTimeUnit('w', time.weeks, compact)} ${getTimeUnit(
      'd',
      time.days,
      compact
    )} ${getTimeUnit('h', time.hours, compact)}`;
  } else {
    return 'Deadline over!';
  }
}

export const DeadlineComponent = (props: IDeadlineProps) => {
  const [date, setDate] = React.useState(
    props.due_date !== null
      ? moment.utc(props.due_date).local().toDate()
      : undefined
  );
  const [displayDate, setDisplayDate] = React.useState(
    getDisplayDate(date, props.compact)
  );
  const [interval, setNewInterval] = React.useState(null);

  React.useEffect(() => {
    const d =
      props.due_date !== null
        ? moment.utc(props.due_date).local().toDate()
        : undefined;
    setDate(d);
    setDisplayDate(getDisplayDate(d, props.compact));
    updateTimeoutInterval(d);
  }, [props]);

  const updateTimeoutInterval = (date: Date) => {
    if (interval) {
      clearInterval(interval);
    }
    const time: ITimeSpec = calculateTimeLeft(date);
    const timeout = time.weeks === 0 && time.days === 0 ? 1000 : 10000;
    const newInterval = setInterval(() => {
      setDisplayDate(getDisplayDate(date, props.compact));
    }, timeout);
    setNewInterval(newInterval);
  };

  return date === undefined ? (
    <Chip
      sx={props.sx}
      size="small"
      icon={<AccessAlarmRoundedIcon />}
      label={'No Deadline 😁'}
    />
  ) : (
    <Chip
      sx={props.sx}
      size="small"
      icon={<AccessAlarmRoundedIcon />}
      label={displayDate}
    />
  );
};
