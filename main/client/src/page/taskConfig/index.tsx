import { ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import React, { useState } from "react";
import './index.less'
import { taskTypeOptions } from "../task";
import { doSyncImages } from "../../call";
import { message } from "antd";
const { useOptionFormListHook } = ChUtils.chHooks


function usePageStore() {

    const { optionsMap: deviceMap, options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {} })
    return {
        deviceMap,
        deviceOptions
    }
}

function TaskConfig() {
    const [syncImageloading, setSyncImageloading] = useState(false)
    const pageStore = usePageStore()
    return <div className="page config-page">
        <ChTablePanel
            actions={[
                {
                    text: '同步图片到本地',
                    type: "default",
                    onClick: () => {
                        if (!syncImageloading) {
                            ChUtils.Ajax.request({
                                url: '/api/config/get_all_config_image',
                                data: {},
                                method: "post"
                            }).then(res => {
                                if (res.status == 0) {
                                    console.log(res);
                                    setSyncImageloading(true)
                                    const files = res.list.map((item: any) => item.path)
                                    console.log('files', files);
                                    res = doSyncImages(files)
                                    if (res.status == 0) {
                                        message.success('同步成功')
                                        setSyncImageloading(false)
                                    }
                                }
                            })
                        }
                    },
                    loading: syncImageloading,

                }
            ]}
            onEditBefore={(data) => {
                console.log(data);
                if (data.url.file && data.url.file.response.data) {
                    data.url = data.url.file.response.data
                }
            }}
            url="/api/config/get_config_image_page"
            urlAdd="/api/config/create_config_image"
            urlDelete="/api/config/delete_config_image_by_id"
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
                    type: FormItemType.select,
                    options: pageStore.deviceOptions,
                    name: 'deviceId',
                    label: '所属设备'
                },
                {
                    type: FormItemType.upload,
                    uploadurl: 'http://103.100.210.203:3000/api/upload/upload_file',
                    uploadname: 'file',
                    uploadType: 'picture',
                    uploadheader: {
                        token: localStorage.getItem('token')
                    },
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
                    title: '所属设备',
                    dataIndex: 'deviceId',
                    key: 'deviceId',
                    render: (v) => <span>{pageStore.deviceMap[v] && pageStore.deviceMap[v].name}</span>
                }, {
                    title: '远程路径',
                    dataIndex: 'url',
                    key: 'url',
                    render: (img) => <img alt='' width="auto" height={25} src={img} />
                }
            ]}
        />
    </div>
}

export default TaskConfig
