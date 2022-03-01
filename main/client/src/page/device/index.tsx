import {Button, Dropdown, Menu, message, Modal} from 'antd';
import React, {useRef, useState} from "react";
import './index.less'
import {ChForm, ChTablePanel, FormItemType, ChUtils} from "ch-ui";
import {DownOutlined} from '@ant-design/icons';
import {useForm} from "antd/es/form/Form";
import {TDevice} from "../../typing";
const { useOptionFormListHook } = ChUtils.chHooks
const request = ChUtils.Ajax.request

function Device() {
    const pageStore = useDevicePageStore()
    return <div className='device'>
        <ChTablePanel
            ref={pageStore.tableRef}
            disablePagination
            columns={[
                {
                    title: '名称',
                    dataIndex: 'name',
                    key: 'name',
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
                    render: (touchId:string)=><div style={{width: '200px'}}>{touchId}</div>
                },
                {
                    title: '品牌',
                    dataIndex: 'brand',
                    key: 'brand',
                },
                {
                    title: '机器人',
                    dataIndex: 'robotName',
                    key: 'robotName',
                },
                {
                    title: '机器人ID',
                    dataIndex: 'robotId',
                    key: 'robotId',
                },
                {
                    title: '机器人是否在线',
                    dataIndex: 'online',
                    key: 'online',
                    render: (online, ob)=> <div>{ob.online ? '在线': '离线'}</div>
                },
                {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                },
                {
                    title: '操作',
                    dataIndex: 'option',
                    key: 'option',
                    render: (_, ob: TDevice)=>{
                        return <div>
                            <Dropdown overlay={
                                <Menu>
                                    <Menu.Item>
                                        <Button onClick={()=>pageStore.handleClickLinkDevice(ob)} type='link'> 连接设备 </Button>
                                    </Menu.Item>
                                    <Menu.Item>
                                        <Button type='link'> 暂停脚本 </Button>
                                    </Menu.Item>
                                    <Menu.Item>
                                        <Button type='link'> 终止脚本 </Button>
                                    </Menu.Item>
                                </Menu>
                            }>
                                <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>
                                    脚本操作<DownOutlined />
                                </a>
                            </Dropdown>
                        </div>
                    }
                }
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
                },{
                    type: FormItemType.select,
                    label: '状态',
                    name: 'status',
                    key: 'status',
                    options: [{
                        label: '空闲',
                        value: '空闲',
                    },{
                        label: '任务中',
                        value: '任务中',
                    }]
                }
            ]}/>
    </div>
}

function useDevicePageStore() {
    const [isAddTaskModalVisible, setIsAddTaskModalVisible] = useState(false);
    const {options: accountOptions} = useOptionFormListHook({url: '/api/game_account/get_game_account_options', query: {}, expiresTime: 5})
    const {options: deviceOptions} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}, expiresTime: 5})
    const tableRef = useRef<{
        reload: Function
    }>()
    const [formRef] = useForm()
    function handleClickLinkDevice(device: TDevice) {
        const owurl = `http://vnc.kukechen.top/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        const tmp:any = window.open(owurl, "",  'height=740, width=360, top=0, left=0')
        tmp.focus();
    }
    function handleCreateTask() {
        setIsAddTaskModalVisible(true)
    }
    function handleCloseCreateTaskModal() {
        setIsAddTaskModalVisible(false)
    }
    function handleSaveTask() {
        formRef.validateFields().then((res:any)=>{
            request({
                url: '/api/task/create_task',
                data: {
                    name: "主线打图",
                    deviceId: res.deviceId,
                    accountId: res.accountId,
                },
                method: "post"
            }).then(res=>{
                if(res.status === 0) {
                    handleCloseCreateTaskModal()
                    message.success('任务创建成功')
                    tableRef.current!.reload()
                }
            })
        })
    }

    return {
        formRef,
        deviceOptions,
        accountOptions,
        handleSaveTask,
        handleCloseCreateTaskModal,
        handleCreateTask,
        isAddTaskModalVisible,
        setIsAddTaskModalVisible,
        tableRef,
        handleClickLinkDevice
    }
}

export default Device;
