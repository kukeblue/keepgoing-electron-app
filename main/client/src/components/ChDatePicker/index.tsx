import {DatePicker} from "antd";
import React from "react";
import moment from 'moment'

const format = 'YYYY-MM-DD'

export interface IChDatePickerProps {
    value?: string,
    onChange?: (value: string)=>void
}

function ChDatePicker(props: IChDatePickerProps) {
    const value = props.value ? moment(props.value) : null
    // @ts-ignore
    return <DatePicker style={{width: '100%'}} value={value} onChange={(date, dateStr)=>props.onChange && props.onChange(dateStr)}/>
}

export default ChDatePicker
