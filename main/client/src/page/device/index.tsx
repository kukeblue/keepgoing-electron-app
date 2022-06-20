import { Button, Dropdown, Menu, message, Modal, Badge } from 'antd';
import React, { useRef, useState } from "react";
import './index.less'
import { ChForm, ChTablePanel, FormItemType, ChUtils } from "ch-ui";
import { useForm } from "antd/es/form/Form";
import { TDevice } from "../../typing";
import html2canvas from 'html2canvas';
const { useOptionFormListHook } = ChUtils.chHooks
const request = ChUtils.Ajax.request

function Device() {
    const pageStore = useDevicePageStore()
    return <div className='device page'>
        <div className='flex'>
            <div className='device-list'>
                <ChTablePanel
                    ref={pageStore.tableRef}
                    disablePagination
                    columns={[
                        {
                            title: '名称',
                            dataIndex: 'name',
                            key: 'name',
                            render: (name, ob) => {
                                return <div style={{ width: '120px' }}>
                                    <Dropdown trigger={['click']} overlay={
                                        <Menu>
                                            <Menu.Item onClick={() => pageStore.handleClickPreviewDevice(ob)}>
                                                <Button type='link'>预览</Button>
                                            </Menu.Item>
                                            <Menu.Item onClick={() => pageStore.handleClickReadToken()}>
                                                <Button type='link'>获取将军令</Button>
                                            </Menu.Item>
                                            <Menu.Item onClick={() => pageStore.handleClickLinkDevice(ob)}>
                                                <Button type='link'> 连接设备 </Button>
                                            </Menu.Item>
                                            <Menu.Item>
                                                <Button type='link'>停止进行的任务</Button>
                                            </Menu.Item>
                                        </Menu>
                                    }>
                                        <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>
                                            <div style={{ width: '150px' }}>{ob.status === '任务中' ? <Badge status="success" /> : <Badge status="default" />}
                                                {name}
                                            </div>
                                        </a>
                                    </Dropdown>
                                </div>
                            },
                            // fixed: true,
                        },
                        {
                            title: '设备类型',
                            dataIndex: 'deviceType',
                            key: 'deviceType',
                            render: (deviceType: string) => <div style={{ width: '100px' }}>{deviceType}</div>
                        },
                        {
                            title: 'IMEI',
                            dataIndex: 'imei',
                            key: 'imei',
                        },
                        {
                            title: 'IP',
                            dataIndex: 'ip',
                            key: 'ip',
                        },
                        {
                            title: '触动设备id',
                            dataIndex: 'touchId',
                            key: 'touchId',
                            render: (touchId: string) => <div style={{ width: '200px' }}>{touchId}</div>
                        },
                        {
                            title: '品牌',
                            dataIndex: 'brand',
                            key: 'brand',
                            render: (brand: string) => <div style={{ width: '120px' }}>{brand}</div>
                        },
                        {
                            title: '状态',
                            dataIndex: 'status',
                            key: 'status',
                            render: (status: string) => <div style={{ width: '120px' }}>{status}</div>
                        },
                    ]}
                    url='/api/device/get_device_page'
                    urlAdd='/api/device/save_device'
                    urlUpdate='/api/device/save_device'
                    urlDelete='/api/device/delete_device'
                    formData={[
                        {
                            type: FormItemType.input,
                            label: '设备名称',
                            name: 'name',
                            key: 'name',
                        },
                        {
                            type: FormItemType.select,
                            label: '设备类型',
                            name: 'deviceType',
                            key: 'deviceType',
                            options: [
                                {
                                    label: '手机',
                                    value: '手机'
                                },
                                {
                                    label: '电脑',
                                    value: '电脑'
                                }
                            ]
                        },
                        {
                            type: FormItemType.input,
                            label: 'imei',
                            name: 'imei',
                            key: 'imei',
                        },
                        {
                            type: FormItemType.input,
                            label: 'ip',
                            name: 'ip',
                            key: 'ip',
                        },
                        {
                            type: FormItemType.input,
                            label: '触动设备号',
                            name: 'touchId',
                            key: 'touchId',
                        },
                        {
                            type: FormItemType.input,
                            label: '品牌',
                            name: 'brand',
                            key: 'brand',
                        },
                        {
                            type: FormItemType.input,
                            label: '机器人名称',
                            name: 'robotName',
                            key: 'robotName',
                        },
                        {
                            type: FormItemType.input,
                            label: '机器人ID',
                            name: 'robotId',
                            key: 'robotId',
                        }, {
                            type: FormItemType.select,
                            label: '状态',
                            name: 'status',
                            key: 'status',
                            options: [{
                                label: '空闲',
                                value: '空闲',
                            }, {
                                label: '任务中',
                                value: '任务中',
                            }]
                        }
                    ]} />
            </div>
            {/*<div className='device-preview'>*/}
            {/*    <div className='device-body'>*/}
            {/*        <iframe frameBorder={0} id='appBody' width='100%' height='100%' src={pageStore.currentPhoneUrl}/>*/}
            {/*    </div>*/}
            {/*    <Button onClick={()=>pageStore.setCurrentPhoneUrl('')} className='m-t-20'>关闭连接</Button>*/}
            {/*    <div>{pageStore.currentPhoneUrl}</div>*/}
            {/*</div>*/}
        </div>
    </div>
}

function useDevicePageStore() {
    const [isAddTaskModalVisible, setIsAddTaskModalVisible] = useState(false);
    const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    const { options: accountOptions } = useOptionFormListHook({ url: '/api/game_account/get_game_account_options', query: {}, expiresTime: 5 })
    const { options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {}, expiresTime: 5 })
    const tableRef = useRef<{
        reload: Function
    }>()
    const [formRef] = useForm()
    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://192.168.0.13:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        const tmp: any = window.open(owurl, "", 'height=1920, width=1080, top=0, left=0')
        tmp.focus();
    }
    const handleClickPreviewDevice = (device: TDevice) => {
        const owurl = `http://192.168.0.13:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const handleClickReadToken = () => {
        // @ts-ignore
        const a = window.document.querySelector('#appBody').querySelector('body')
        console.log(a)
        // @ts-ignore
        html2canvas(window.document.querySelector(body), { useCORS: true }).then(function (canvas) {
            // @ts-ignore
            window.document.querySelector('.device-list').appendChild(canvas);
        });
    }
    function handleCreateTask() {
        setIsAddTaskModalVisible(true)
    }
    function handleCloseCreateTaskModal() {
        setIsAddTaskModalVisible(false)
    }
    function handleSaveTask() {
        formRef.validateFields().then((res: any) => {
            request({
                url: '/api/task/create_task',
                data: {
                    name: "主线打图",
                    deviceId: res.deviceId,
                    accountId: res.accountId,
                },
                method: "post"
            }).then(res => {
                if (res.status === 0) {
                    handleCloseCreateTaskModal()
                    message.success('任务创建成功')
                    tableRef.current!.reload()
                }
            })
        })
    }

    return {
        currentPhoneUrl,
        setCurrentPhoneUrl,
        formRef,
        deviceOptions,
        accountOptions,
        handleSaveTask,
        handleCloseCreateTaskModal,
        handleCreateTask,
        handleClickPreviewDevice,
        isAddTaskModalVisible,
        setIsAddTaskModalVisible,
        tableRef,
        handleClickLinkDevice,
        handleClickReadToken
    }
}

export default Device;
