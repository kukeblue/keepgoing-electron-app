import { ChTablePanel, FormItemType } from "ch-ui";
import React from "react";
import './index.less'

function TaskConfig() {
    return <div className="page config-page">
        <ChTablePanel 
            url="/api/config/get_config_image_page" 
            urlAdd="/api/config/create_config_image"
            formData={[
                {
                    type: FormItemType.input,
                    name: 'name',
                    label: '图片名称'
                },
                {
                    type: FormItemType.input,
                    name: 'path',
                    label: '路径'
                },
                {
                    type: FormItemType.input,
                    name: 'deviceId',
                    label: '所属设备'
                },
                {
                    type: FormItemType.input,
                    name: 'taskId',
                    label: '所属任务'
                },{
                    type: FormItemType.input,
                    name: 'url',
                    label: '图片'
                }
            ]}
            searchFormData={[
                {
                    type: FormItemType.input,
                    name: 'name',
                    label: '图片名称',
                    layout: {
                        span: 4
                    }
                }
            ]}
            columns={[
                {
                    title: '图片名称',
                    dataIndex: 'name',
                    key: 'name', 
                },
                {
                    title: '路径',
                    dataIndex: 'path',
                    key: 'path', 
                },
                {
                    title: '所属任务',
                    dataIndex: 'taskId',
                    key: 'taskId', 
                },{
                    title: '所属设备',
                    dataIndex: 'deviceId',
                    key: 'deviceId', 
                }, {
                    title: '远程路径',
                    dataIndex: 'url',
                    key: 'url', 
                }
            ]}
        />
    </div>
}

export default TaskConfig
