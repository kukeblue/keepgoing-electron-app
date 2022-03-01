import React, {useRef} from "react";
import './index.less'
import {ChTablePanel, ChUtils, FormItemType} from "ch-ui";

function Report() {
    return <div>
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
