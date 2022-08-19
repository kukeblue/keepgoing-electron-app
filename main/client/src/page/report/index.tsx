import React, { useRef } from "react";
import './index.less'
import { ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import { createContainer } from 'unstated-next'
import moment from "moment";

export function usePageStore() {
    return {

    }
}

export const PageStore = createContainer(usePageStore)


function Report() {
    return <div>
        <br />
        <ChTablePanel
            formData={[]}
            url="/api/report/get_report_page"
            columns={[
                {
                    dataIndex: 'date',
                    key: 'date',
                    title: '日期',
                },
                {
                    dataIndex: 'time',
                    key: 'time',
                    title: '时间',
                    render: (v: any) => <div style={{ width: '100px' }}>{moment(v * 1000).format('HH:mm')}</div>
                },
                {
                    dataIndex: 'type',
                    key: 'type',
                    title: '类型',
                },
                {
                    dataIndex: 'gameId',
                    key: 'gameId',
                    title: '角色',
                },
                {
                    dataIndex: 'income',
                    key: 'income',
                    title: '收入',
                },
                {
                    dataIndex: 'expend',
                    key: 'expend',
                    title: '支出',
                }, {
                    dataIndex: 'profit',
                    key: 'profit',
                    title: '毛利润',
                }, {
                    dataIndex: 'note',
                    key: 'note',
                    title: '备注',
                }
            ]}
        />
    </div>
}

export default Report
