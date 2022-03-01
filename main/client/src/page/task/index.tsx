import {Button, DatePicker, Dropdown, Menu, message} from 'antd';
import React, {useRef} from "react";
import './index.less'
import {DownOutlined} from '@ant-design/icons';
import {ChTablePanel, ChUtils, FormItemType} from "ch-ui";
import {TTask} from "../../typing";
import ChDatePicker from "../../components/ChDatePicker";

const { useOptionFormListHook } = ChUtils.chHooks
const request = ChUtils.Ajax.request
function task() {
    const pageStore = useTaskPageStore()
    return <div className='task'>
        <ChTablePanel
            actions={[{
                type: 'primary',
                text: '同步收益',
                onClick: ()=>{pageStore.syncIncome()}
            }]}
            searchFormData={[
                {
                    label: '任务日期',
                    name: 'date',
                    type: FormItemType.date,
                    layout: {
                        span:4
                    }
                }
            ]}
            ref={pageStore.tableRef}
            columns={[
                {
                    title: '任务日期',
                    dataIndex: 'date',
                    key: 'date',
                },
                {
                    title: '任务编号',
                    dataIndex: 'taskNo',
                    key: 'taskNo',
                },
                {
                    title: '任务名称',
                    dataIndex: 'name',
                    key: 'name',
                },
                {
                    title: '设备',
                    dataIndex: 'deviceId',
                    key: 'deviceId',
                    render:(v)=><div>{pageStore.deviceMap[v].name}</div>
                },
                {
                    title: '角色',
                    dataIndex: 'accountId',
                    key: 'accountId',
                    render:(v)=><div>{pageStore.accountMap[v] && pageStore.accountMap[v].name}</div>
                },
                {
                    title: '开始时间',
                    dataIndex: 'startTime',
                    key: 'startTime',
                    render: (_, o)=> <div>{!o.startTime ? "" : ChUtils.chFormats.formatDate(o.startTime *1000, 'YY-MM-DD hh:mm:ss')}</div>
                },
                {
                    title: '结束时间',
                    dataIndex: 'endTime',
                    key: 'endTime',
                    render: (_, o)=> <div>{!o.endTime ? "" : ChUtils.chFormats.formatDate(o.endTime *1000, 'YY-MM-DD hh:mm:ss')}</div>
                },
                {
                    title: '最后更新时间',
                    dataIndex: 'updateTime',
                    key: 'updateTime',
                    render: (_, o)=> <div>{!o.updateTime ? "" : ChUtils.chFormats.formatDate(o.updateTime *1000, 'YY-MM-DD hh:mm:ss')}</div>
                },
                {
                    title: '状态',
                    dataIndex: 'status',
                    key: 'status',
                },
                {
                    title: '任务次数',
                    dataIndex: 'taskCount',
                    key: 'taskCount',
                },
                {
                    title: '预计收入',
                    dataIndex: 'income',
                    key: 'income',
                },
                {
                    title: '任务日志',
                    dataIndex: 'note',
                    key: 'note',
                },
                {
                    title: '操作',
                    dataIndex: 'option',
                    key: 'option',
                    render: (_, task: TTask)=>{
                        return <div>
                            {/*<Button type='link'>任务记录</Button>*/}
                            <Dropdown overlay={
                                <Menu>
                                    <Menu.Item>
                                        <Button onClick={()=>{pageStore.startTask(task)}} type='link'> 执行任务 </Button>
                                    </Menu.Item>
                                    <Menu.Item>
                                        <Button onClick={()=>{pageStore.stopTask(task)}} type='link'> 停止任务 </Button>
                                    </Menu.Item>
                                </Menu>
                            }>
                                <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>
                                    操作<DownOutlined />
                                </a>
                            </Dropdown>
                        </div>
                    }
                }
            ]}
            url='/api/task/get_task_page'
            urlAdd='/api/task/create_task'
            urlDelete='/api/task/delete_task_by_id'
            formData={[
                {
                    type: FormItemType.select,
                    label: '任务类型',
                    name: 'name',
                    key: 'name',
                    options: [
                        {
                            label: '主线打图',
                            value: '主线打图'
                        }
                    ]
                },
                {
                    type: FormItemType.select,
                    label: '设备',
                    name: 'deviceId',
                    key: 'deviceId',
                    options: pageStore.deviceOptions
                },
                {
                    type: FormItemType.select,
                    label: '账号',
                    name: 'accountId',
                    key: 'accountId',
                    options: pageStore.accountOptions
                }
            ]}/>
    </div>
}

function useTaskPageStore() {
    const {optionsMap: accountMap, options: accountOptions} = useOptionFormListHook({url: '/api/game_account/get_game_account_options', query: {}})
    const {optionsMap: deviceMap, options: deviceOptions} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}})
    const tableRef = useRef<{
        reload: Function
    }>()
    const stopTask = function(item: TTask) {
        request({
            url: '/api/task/stop_task',
            data: {
                id: item.id,
                deviceId: item.deviceId,
                accountId: item.accountId,
            },
            method: "post"
        }).then(res=>{
            if(res.status === 0) {
                message.success('任务停止成功')
                tableRef.current!.reload()
            }
        })
    }
    const syncIncome = function() {
        request({
            url: '/api/task/calculate_income',
            data: {},
            method: "get"
        }).then(res=>{
            if(res.status === 0) {
                message.success('同步收益成功！')
            }
        })
    }
    const startTask = function(item: TTask) {
        request({
            url: '/api/task/start_task',
            data: {
                id: item.id,
                deviceId: item.deviceId,
                accountId: item.accountId,
            },
            method: "post"
        }).then(res=>{
            if(res.status === 0) {
                message.success('任务执行成功')
                tableRef.current!.reload()
            }
        })
    }

    return {
        syncIncome,
        stopTask,
        startTask,
        tableRef,
        accountMap,
        deviceMap,
        accountOptions,
        deviceOptions
    }
}

export default task;
