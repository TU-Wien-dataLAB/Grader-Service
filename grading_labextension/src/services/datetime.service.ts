import moment from 'moment';

// 2021-09-03T11:57
export function localToUTC(time: string): string {
    return moment(time).utc().format('YYYY-MM-DDTHH:mm:ss.sss') + "Z";
}

export function utcToLocal(time: string): string {
    return moment.utc(time).local().format('YYYY-MM-DDTHH:mm:ss.sss')
}

export function utcToLocalFormat(time: string): string {
    const localeData = moment.localeData("de");
    const format = localeData.longDateFormat('L') + ' HH:mm:ss';
    return moment.utc(time).local().format(format)
}

export function utcToTimestamp(time: string): number {
    return moment(time, 'YYYY-MM-DDTHH:mm:ss.sss').valueOf();
}