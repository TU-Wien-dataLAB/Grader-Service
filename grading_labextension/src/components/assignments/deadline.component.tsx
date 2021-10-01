import * as React from 'react';
import { Tag } from "@blueprintjs/core";
import moment from 'moment';

export interface DeadlineProps {
    due_date: string
}

interface TimeSpec {
    weeks: number,
    days: number,
    hours: number,
    minutes: number,
    seconds: number
}

// 2021-06-06 23:59:00
export class DeadlineComponent extends React.Component<DeadlineProps> {
    public interval: number = null;
    public state = {
        date: null as Date,
        display_date: ""
    };

    constructor(props: DeadlineProps) {
        super(props);
        this.state.date = moment.utc(props.due_date).local().toDate();
        this.state.display_date = this.getDisplayDate();
    }

    public componentWillReceiveProps(nextProps: DeadlineProps) {
        this.setState({
            display_date: this.getDisplayDate(),
            date: moment.utc(nextProps.due_date).local().toDate()
        });
        this.updateTimeoutInterval();
    }

    public componentDidMount() {
        this.updateTimeoutInterval();
    }

    private updateTimeoutInterval() {
        if (this.interval) clearInterval(this.interval);
        let time: TimeSpec = this.calculateTimeLeft();
        let timeout = (time.weeks == 0 && time.days == 0) ? 1000 : 10000;
        this.interval = setInterval(() => {
            this.setState({ display_date: this.getDisplayDate() });
        }, timeout);
    }

    public calculateTimeLeft = () => {
        let difference = +this.state.date - +new Date();
        let timeLeft: TimeSpec = {
            weeks: Math.floor(difference / (1000 * 60 * 60 * 24 * 7)),
            days: Math.floor(difference / (1000 * 60 * 60 * 24) % 7),
            hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
            minutes: Math.floor((difference / 1000 / 60) % 60),
            seconds: Math.floor((difference / 1000) % 60)
        }
        return timeLeft;
    }

    public getDisplayDate(): string {
        let time: TimeSpec = this.calculateTimeLeft();
        if (time.weeks == 0) {
            if (time.days == 0) {
                return `Deadline in ${this.getTimeUnit("Hour", time.hours)} ${this.getTimeUnit("Minute", time.minutes)} ${this.getTimeUnit("Second", time.seconds)}`;
            } else {
                return `Deadline in ${this.getTimeUnit("Day", time.days)} ${this.getTimeUnit("Hour", time.hours)} ${this.getTimeUnit("Minute", time.minutes)}`;
            }

        } else if (time.weeks > 0) {
            return `Deadline in ${this.getTimeUnit("Week", time.weeks)} ${this.getTimeUnit("Day", time.days)} ${this.getTimeUnit("Hour", time.hours)}`;
        } else {
            return "Deadline over!";
        }
    }

    private getTimeUnit(text: string, value: number): string {
        if (value == 1) return `${value} ${text}`;
        else return `${value} ${text}s`;
    }

    public render() {
        return <Tag intent="warning" htmlTitle={"Date: " + this.state.date.toLocaleDateString() + " " + this.state.date.toLocaleTimeString()} style={{ marginLeft: "10px" }} >{this.state.display_date}</Tag>
    }
}