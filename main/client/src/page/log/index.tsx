import {Tag, Popconfirm, Switch} from 'antd';
import React, {useRef, useState} from "react";
import './index.less'
import {ChTablePanel, ChUtils, FormItemType} from "ch-ui";
import {TTaskLog} from "../../typing";
import mp3_error from "../../assets/mp3/error.mp3";


const logTypeOptions = [
    {
        label: 'info',
        value: 'info',
    },{
        label: '启动',
        value: 'launch',
    },{
        label: 'warning',
        value: 'warn',
    },{
        label: '异常',
        value: 'error',
    },{
        label: '完成',
        value: 'finish',
    }
]

const logTypeMap = {
    'info': 'info',
    'launch': '启动',
    'warn': 'warning',
    'error': '异常',
    'finish': '完成',
}

const { useOptionFormListHook, useInterval } = ChUtils.chHooks
function Log() {
    const pageStore = useLogPageStore()
    useInterval(
        () => {
            if(pageStore.openRefresh) {
                pageStore.tableRef.current!.reload()
            }
        },
        10000
    )
    return <div className='home'>
        <audio id="tip">
            <source src="//blackhole9527.oss-cn-zhangjiakou.aliyuncs.com/7xmeu-6d9ll.mp3"/>
            <source  src="//blackhole9527.oss-cn-zhangjiakou.aliyuncs.com/7xmeu-6d9ll.mp3"/>
            <embed height="50" width="100" src="//blackhole9527.oss-cn-zhangjiakou.aliyuncs.com/7xmeu-6d9ll.mp3"/>
        </audio>

        <ChTablePanel
            onReloadAfter={pageStore.onReloadAfter}
            ref={pageStore.tableRef}
            searchFormData={[
                {
                    label: '角色',
                    name: 'accountId',
                    type: FormItemType.select,
                    options: pageStore.accountOptions,
                    layout: {
                        span: 4
                    }
                },
                {
                    label: '类型',
                    name: 'type',
                    type: FormItemType.select,
                    options: logTypeOptions,
                    layout: {
                        span: 4,
                        offset:1
                    }
                }, {
                    label: '开启自动刷新',
                    name: 'option',
                    type: FormItemType.other,
                    dom: <Switch checked={pageStore.openRefresh}  onChange={(v: boolean)=>{
                        pageStore.setOpenRefresh(v)
                    }} />,
                    layout: {
                        span: 4,
                        offset:1
                    }
                }
            ]}
            columns={[
                {
                    title: '时间',
                    dataIndex: 'time',
                    key: 'time',
                    render: (_, o)=> <div>{!o.time ? "" : ChUtils.chFormats.formatDate(o.time *1000, 'YY-MM-DD hh:mm:ss')}</div>
                },
                {
                    title: '任务编号',
                    dataIndex: 'taskNo',
                    key: 'taskNo',
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
                    render:(v)=><div>{pageStore.accountMap[v].name}</div>
                },
                {
                    title: '类型',
                    dataIndex: 'type',
                    key: 'type',
                    render: (v, taskLog:TTaskLog)=> {
                        let ret = <></>
                        switch (v) {
                            case 'info':
                                ret =  <Tag color="#108ee9">info</Tag>
                                break
                            case 'launch':
                                ret =  <Tag color="#87d068">启动</Tag>
                                break
                            case 'warn':
                                ret = <Tag color="orange">warning</Tag>
                                break
                            case 'error':
                                ret = <Popconfirm placement="topLeft" title='是否连接设备' onConfirm={()=>{
                                    const ip = pageStore.deviceMap[taskLog.deviceId].ip
                                    const owurl = `http://vnc.kukechen.top/vnc.html?host=${ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
                                    const tmp:any = window.open(owurl, "",  'height=360, width=740, top=0, left=0')
                                    tmp.focus();
                                }} okText="确定" cancelText="取消">
                                        <Tag style={{ cursor: 'pointer' }} color="#f50">异常</Tag>
                                    </Popconfirm>
                                break
                            case 'finish':
                                ret = <Tag color="#87d068">完成</Tag>
                                break
                        }
                        return ret
                    }
                },
                {
                    title: '任务次数',
                    dataIndex: 'taskCount',
                    key: 'taskCount',
                    render:(v)=><div>{Number(v)>0 ? v : '--'}</div>
                },
                {
                    title: '备注',
                    dataIndex: 'note',
                    key: 'note',
                },
            ]}  url='/api/task_log/get_task_log_page'
            formData={[]}/>
    </div>
}

function useLogPageStore() {
    const [openRefresh, setOpenRefresh] = useState(false)
    const {optionsMap: accountMap, options: accountOptions} = useOptionFormListHook({url: '/api/game_account/get_game_account_options', query: {}})
    const {optionsMap: deviceMap} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}})
    const tableRef = useRef<{
        reload: Function
        _query: Object,
    }>()
    const onReloadAfter = (resp: {page: {list: TTaskLog[]}}) => {
        if(resp.page.list.length > 0) {
            const log = resp.page.list[0]
            if(log.type == "error") {
                playMp3()
            }else {
                // stopMp3()
            }
        }
    }
    const playMp3 = () => {
        const audio: any = document.getElementById("tip");
        audio.play();
    }

    const stopMp3 = () => {
        const audio: any = document.getElementById("tip");
        audio.stop();
    }

    return {
        playMp3,
        stopMp3,
        tableRef,
        accountMap,
        deviceMap,
        accountOptions,
        onReloadAfter,
        setOpenRefresh,
        openRefresh
    }
}

export default Log;
