import React, { useRef } from "react";
import './index.less'
import { ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import { createContainer } from 'unstated-next'

export function usePageStore() {
    return {

    }
}

export const PageStore = createContainer(usePageStore)


function Report() {
    return <div>
        <div>
            价格配置
        </div>
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
                    dataIndex: 'income',
                    key: 'income',
                    title: '收入',
                },
                {
                    dataIndex: 'expend',
                    key: 'expend',
                    title: '支出',
                }
            ]}
        />
    </div>
}

export default Report
