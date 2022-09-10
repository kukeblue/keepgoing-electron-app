import React, { useRef, useState } from "react";
import './index.less'
import { ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import { createContainer } from 'unstated-next'
import moment from "moment";
import Ajax from "ch-ui/dist/chutils/request";
import { message } from "antd";
const request = ChUtils.Ajax.request

export function usePageStore() {
    const [syncIncomeLoading, setSyncIncomeLoading] = useState(false)
    const syncIncome = function () {
        setSyncIncomeLoading(true)
        request({
            url: '/api/report/build_report_day_summary',
            data: {},
            method: "post"
        }).then((res: { status: number; }) => {
            if (res.status === 0) {
                setSyncIncomeLoading(false)
                message.success('同步收益成功！')
            }
        })
    }
    return {
        syncIncome,
        syncIncomeLoading,
        setSyncIncomeLoading
    }
}

export const PageStore = createContainer(usePageStore)


function Report() {
    const pageStore = PageStore.useContainer()
    return <div>
        <br />
        <ChTablePanel
            actions={[{
                loading: pageStore.syncIncomeLoading,
                type: 'primary',
                text: '同步收益',
                onClick: () => { pageStore.syncIncome() }
            }]}

            searchFormData={[
                {
                    label: '日期',
                    name: 'date',
                    initialValue: moment().format('YYYY-MM-DD'),
                    type: FormItemType.date,
                    layout: {
                        span: 4
                    }
                }
            ]}
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

export default () =>
    // @ts-ignore
    <PageStore.Provider><Report /></PageStore.Provider>
