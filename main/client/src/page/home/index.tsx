
import React, { useEffect, useState, useRef } from "react";
import { Drawer, Button, Col, Input, message, Modal, Popover, Row, Select, Switch, Tabs, Collapse, Divider, Badge, Tag } from 'antd'
import { TDevice, TGameAccount, TGameRole, TWatuGroup } from "../../typing";
import "./index.less";
const request = ChUtils.Ajax.request
import { ChForm, ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import { useForm } from "antd/es/form/Form";
import { setClickMode, setOption ,doKillProcess, doStartGame, doTest, doTest2, MainThread, doGetWatuInfo, doZhuaGuiTask, doBee, doGetWatuClickMap, doCloseAllTask, doThrowLitter, doSellEquipment, doConnector, doZhandou, doHanghua, doUpdatePy, doBudianTask } from "../../call";


import { createContainer } from 'unstated-next'
const { TabPane } = Tabs;
const { Panel } = Collapse;
// @ts-ignore
const { confirm } = Modal;
import {
    DownCircleOutlined,
    ClearOutlined,
    CloseCircleOutlined,
    PlusSquareOutlined,
    ScanOutlined,
    SettingOutlined,
    ToolOutlined
    // @ts-ignore
} from '@ant-design/icons';
import ChMhMapTool from "../../components/ChMhMapTool";
import { UserStore } from "../../store/userStore";
import Account from "../account";
import TextArea from "antd/lib/input/TextArea";
import Item from "antd/lib/list/Item";

type TPanelTask = 'test' | 'test2' | 'login' | ''
const { useOptionFormListHook, usePage } = ChUtils.chHooks

type TWatuInfo = {
    mapName: string,
    points: [number, number][]
    deviceId?: number
}
// @ts-ignore
window.isBee = true
// @ts-ignore
window.isChilan = true


let selectDeviceFunc: 'handleSelectJiangjunDevice' | 'handleSelectWatuDevice' | 'handleSelectZhuaGuiDevice'
let watuDeviceId = 0
let zhuaGuiDeviceId = 0
export function usePageStore() {
    const userStore = UserStore.useContainer()
    useEffect(() => {
        MainThread.messageListener.pushLogHandles = [handlePushLog]
        MainThread.messageListener.pushStateHandles = [handlePushState]
        MainThread.messageListener.methodGetWatuInfoReplyHandles = [handleGetWatuInfoReply]
        // @ts-ignore
        window.cangkuPath = '建邺城'
        request({
            url: '/api/task/task_lock',
            data: {},
            method: "post"
        }).then(res => {
            if (res.status != 0) {
                setLock(false)
            }
        }).catch(() => {
            setLock(false)
        })
            setTimeout(()=>{
                const id = userStore.user?.id
                if(id) {
                setOption(id)
            }
            }, 1000)
        
    }, [])
    const [showLog, setShowLog] = useState<boolean>(false)
    const [logs, setLogs] = useState<string[]>([])
    useEffect(() => {
        // setLogs([])
    }, [showLog])

    const [lock, setLock] = useState<boolean>(true)
    const [processState, setProcessState] = useState({
        runningPyProcess: {}
    })
    const [formRef] = useForm()
    const [modalMultipleAccountSelectShow, setModalMultipleAccountSelectShow] = useState(false)
    const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    const [featureTabIndex, setFeatureTabIndex] = useState("2");
    const [isTasking, setIsTasking] = useState<boolean>(false)
    const [isShowHanhu, setsShowHanhu] = useState<boolean>(false)
    const [isBee, setIsBee] = useState<boolean>(true)
    // 是否吃蓝
    const [isChilan, setIsChilan] = useState<boolean>(true)
    // 开启硬件模拟
    const [isYinjian, setIsYinjian] = useState<boolean>(false)
    const [isBigGhost, setIsBigGhost] = useState<boolean>(true)
    const [isAccept, setIsAccept] = useState<boolean>(true)
    const [cangkuPath, setCangkuPath] = useState<string>('建邺城');
    const [currentTask, setCurrentTask] = useState<TPanelTask>('')
    const [code, setCode] = useState<number>()
    const [watuInfo, setWatuInfo] = useState<TWatuInfo>()
    const [linkDeviceId, setLinkDeviceId] = useState<number | undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const { optionsMap: deviceMap, options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {} })
    const { optionsMap: accountMap, options: accountOptions, list: accountList } = useOptionFormListHook({ url: '/api/game_account/get_game_account_options', query: {} })
    const handlePushLog = (log: string) => {
        setLogs((logs) => [...logs, log])
    }
    const handlePushState = (processState: any) => { setProcessState(processState) }
    const handleClickPreviewDevice = (device: TDevice) => {
        const owurl = `http://192.168.0.11:8888/vnc.html?host=192.168.8.120&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://192.168.0.11:8888/vnc.html?host=${device.ip}&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
        setTimeout(() => {
            // @ts-ignore
            window.document.querySelector('.home-device-body').scrollTop = 64
        }, 1000)
    }
    const handleKillProcess = (pid: string) => {
        doKillProcess(pid)
        message.success('操作成功')
    }
    const handleGetWatuInfo = (restart = 0) => {
        if (isBee) {
            setShowLog(true)
            message.success('操作成功')
            // @ts-ignore
            doBee(cangkuPath, restart, window.isChilan)
        } else {
            setShowLog(true)
            message.success('操作成功')
            // @ts-ignore
            doGetWatuInfo(window.isChilan)
        }
    }
    const doTaskAuth = (callback: Function) => {
        request({
            url: '/api/task/do_task_auth',
            data: {},
            method: "post"
        }).then(res => {
            if (res.status != 0) {
                message.info('暂无使用权限')
            } else {
                callback()
            }
        })
    }
    const closeAllTask = () => {
        setShowLog(false)
        message.success('清理后台脚本');
        doCloseAllTask()
    }
    const throwLitter = () => {
        setShowLog(true)
        message.success('操作成功');
        doThrowLitter(watuDeviceId)
    }
    const sellEquipment = () => {
        setShowLog(true)
        message.success('操作成功');
        doSellEquipment(watuDeviceId)
    }
    const handleGetWatuInfoReply = (data: any) => {

        const result = data.result
        let mapName = ''
        let mostName = 0
        let mapNameCounts: any = {
        }
        result.map((item: any) => {
            let mapName = item[0]
            if (!mapNameCounts[mapName]) {
                mapNameCounts[mapName] = 1
            } else {
                mapNameCounts[mapName] = mapNameCounts[mapName] + 1
            }
        })
        Object.keys(mapNameCounts).map(key => {
            let mapNameCount = mapNameCounts[key]
            if (mostName < mapNameCount) {
                mostName = mapNameCount
                mapName = key
            }
        })
        const points = result.map((item: any) => {
            return item[1]
        })
        console.log('handleGetWatuInfoReply:', points);
        setWatuInfo({
            mapName,
            points,
            deviceId: watuDeviceId,
        })
        // @ts-ignore
        // @ts-ignore
        if (window.isBee) {
            console.log('直接开始挖图');
            // @ts-ignore
            console.log(window.beeData)
            // @ts-ignore
            doGetWatuClickMap(...window.beeData, true, window.cangkuPath, window.isChilan)
        }
    }

    const handleSelectJiangjunDevice = () => {
        formRef.validateFields().then((res: any) => {
            if (res.deviceId) {
                const device: TDevice = deviceMap[res.deviceId]
                handleClickLinkDevice(device)
                setShowSelectDeviceModal(false)
                message.success('导入将军令中，请稍后...')
            }
        })
    }
    // const handleSelectWatuDevice = () => {
    //     formRef.validateFields().then((res: any) => {
    //         if (res.deviceId) {
    //             if (res.acceptId) {
    //                 // @ts-ignore
    //                 window.acceptId = res.acceptId
    //             }
    //             watuDeviceId = res.deviceId
    //             handleGetWatuInfo()
    //             setShowSelectDeviceModal(false)
    //         }
    //     })
    // }
    const handleTest = () => checkIsTasking(() => {
        setCurrentTask('test')
        setIsTasking(true)
        setShowLog(true)
        const res = doTest()
        if (res.status == 0) {
            message.success('连接成功')
            setIsTasking(false)
        }
    })
    const handleTest2 = () => checkIsTasking(() => {
        setCurrentTask('test2')
        setIsTasking(true)
        const res = doTest2()
        setShowLog(true)
        if (res.status == 0) {
            message.success('测试已提交')
            setIsTasking(false)
        }
    })
    const handleClearLog = () => {
        setLogs([])
    }
    const checkIsTasking = (cb: Function) => {
        if (!isTasking) {
            cb()
        } else {
            message.warn('当前有任务进行中')
        }
    }
    const getTaskLoading = (task: TPanelTask) => {
        return isTasking && task === currentTask
    }
    const logAllAccount = (type: number) => {
        if (type === 1) {
            doStartGame(['ch1993com5', 'ch.1993.com', 'ch1993com6', 'ch1993com8', 'ch1993com1'])
            message.success('启动成功')
        } else {
            doStartGame(['ch1993com2', 'ch1993com3', 'ch1993com4', 'ch1993com7', 'mm1042061794'])
            message.success('启动成功')
        }
    }
    const handleChangeIsBeen = (check: boolean) => {
        setIsBee(check);
        // @ts-ignore
        window.isBee = check;
    }

    const handleChangeIsChilan = (check: boolean) => {
        setIsChilan(check);
        // @ts-ignore
        window.isChilan = check;
        // @ts-ignore
        print(window.isChilan)
    }

    const connector = () => {
        setShowLog(true)
        message.success('操作成功')
        doConnector()
    }
    const zhandou = () => {
        setShowLog(true)
        message.success('操作成功')
        doZhandou(watuDeviceId)
    }
    const hanghua = () => {
        setShowLog(true)
        message.success('操作成功')
        // @ts-ignore
        doHanghua(window.hanghuaCount)
    }
    const 弹出添加分组框 = () => {
    }
    const 更新脚本 = () => {

    }
    const handleChangeIsYinjian = (v: boolean) => {
        setIsYinjian(v)
        if(v) {
           setClickMode(2)
        }else {
            setClickMode(1)
        }
    }
    return {
        doTaskAuth,
        handleChangeIsChilan,
        setIsChilan,
        isYinjian,
        setIsYinjian,
        handleChangeIsYinjian,
        isChilan,
        setShowLog,
        showLog,
        setIsBigGhost,
        isBigGhost,
        弹出添加分组框,
        lock,
        featureTabIndex, // 激活的功能tab栏
        setFeatureTabIndex,
        setsShowHanhu,
        isShowHanhu,
        setCangkuPath,
        cangkuPath,
        zhandou,
        connector,
        sellEquipment,
        throwLitter,
        closeAllTask,
        isBee,
        setIsBee,
        setModalMultipleAccountSelectShow,
        modalMultipleAccountSelectShow,
        accountMap,
        accountOptions,
        accountList,
        handleKillProcess,
        processState,
        logs,
        isTasking,
        logAllAccount,
        handleClickPreviewDevice,
        formRef,
        linkDeviceId,
        setLinkDeviceId,
        watuInfo,
        setWatuInfo,
        deviceOptions,
        handleClickLinkDevice,
        handleSelectJiangjunDevice,
        handleClearLog,
        showSelectDeviceModal,
        setShowSelectDeviceModal,
        currentPhoneUrl,
        setCurrentPhoneUrl,
        setCode,
        code,
        handleTest,
        handleTest2,
        getTaskLoading,
        handleGetWatuInfo,
        handleChangeIsBeen,
        hanghua
    }
}
export const PageStore = createContainer(usePageStore)
export const HomePageStore = PageStore
function ModalMultipleAccountSelect() {
    const pageStore = PageStore.useContainer()
    const [formRef] = useForm()
    const handleOk = () => {
        formRef.validateFields().then((res: any) => {
            if (res.accounts) {
                const ret = res.accounts.map((accountId: number) => {
                    return pageStore.accountMap[accountId].username
                })
                pageStore.setShowLog(true)
                message.success('操作成功')
                doStartGame(ret)

            }
            formRef.resetFields()
            pageStore.setModalMultipleAccountSelectShow(false)
        })
    }
    return <Modal onOk={handleOk} visible={pageStore.modalMultipleAccountSelectShow} onCancel={() => pageStore.setModalMultipleAccountSelectShow(false)}>
        <ChForm form={formRef} formData={[{
            label: '选择账号',
            name: 'accounts',
            type: FormItemType.multipleSelect,
            options: pageStore.accountOptions
        }]} />
    </Modal>

}
function HomeGameArea() {
    const pageStore = PageStore.useContainer()
    const hadleSubmitDevice = () => {
        if (selectDeviceFunc === 'handleSelectJiangjunDevice') {
            pageStore.handleSelectJiangjunDevice()
        } else if (selectDeviceFunc === 'handleSelectWatuDevice') {
        }

    }
    const runningPyProcess = pageStore.processState.runningPyProcess || {}
    return <div className='login-game-area'>
        <div className='flex-row-center'>
            <Drawer visible={pageStore.showLog} onClose={() => {
                pageStore.closeAllTask()
                pageStore.setShowLog(false)
            }}>
                <div className='flex-row-center m-b-20'>
                    {/* <Button icon={<ScanOutlined />} className='fs-12' size="small" onClick={() => {
                        selectDeviceFunc = 'handleSelectJiangjunDevice'
                        pageStore.setShowSelectDeviceModal(true)
                    }}>导入将军令</Button> */}
                    {/* <Button icon={<CloseCircleOutlined />} className='fs-12 m-l-5' size="small" onClick={() => { pageStore.setCurrentPhoneUrl(''); message.success('关闭成功') }}>关闭连接</Button> */}
                    <Button icon={<CloseCircleOutlined />} className='fs-12 m-l-5' size="small" onClick={() => { pageStore.closeAllTask() }}>关闭脚本</Button>
                    <Button icon={<ClearOutlined />} className='fs-12 m-l-5' size="small" onClick={() => {
                        pageStore.handleClearLog()
                    }}>清空日志</Button>
                    {/*<div>{pageStore.currentPhoneUrl}</div>*/}

                    {/*<Button className={'m-l-20'} type={"primary"} onClick={()=>{*/}
                    {/*    pageStore.logAllAccount(2)*/}
                    {/*}}>一件启动2号队伍</Button>*/}
                </div>
                <div className='home-device-preview'>
                    <div className='home-device-body'>
                        <iframe frameBorder={0} id='appBody' src={pageStore.currentPhoneUrl} />
                    </div>
                </div>
                <div id='home-log-panel' className='home-log-panel'>
                    <div className='home-log-panel-setting'>
                        <Popover placement="bottom" title={'任务管理器'} content={
                            <div style={{ width: 300 }}>
                                <p style={{ color: '#666' }}>{Object.keys(runningPyProcess).length}进行中的python进程</p>
                                {Object.keys(runningPyProcess).map(key => {
                                    return <div key={key} className='flex-between'>
                                        <div>{key}</div>
                                        <div>{
                                            // @ts-ignore
                                            runningPyProcess[key]
                                        }</div>
                                        <Button onClick={() => pageStore.handleKillProcess(
                                            // @ts-ignore
                                            runningPyProcess[key]
                                        )
                                        } type={'link'}>结束进程</Button>
                                    </div>
                                })}
                            </div>
                        } trigger="click">
                            <SettingOutlined size={25} />
                        </Popover>
                    </div>
                    {pageStore.logs.map((item: string, index: number) => {
                        return <div key={`_${index}`}>{item}</div>
                    })}
                </div>
            </Drawer>
        </div >
        <Modal onCancel={() => pageStore.setShowSelectDeviceModal(false)} onOk={() => {
            hadleSubmitDevice()
        }} visible={pageStore.showSelectDeviceModal}>
            <div>
                <ChForm form={pageStore.formRef} formData={[
                    {
                        type: FormItemType.select, label: '选择设备', name: 'deviceId', options: pageStore.deviceOptions
                    }, {
                        type: FormItemType.input, label: '接货角色Id', name: 'acceptId'
                    },
                ]} />
            </div>
        </Modal>
    </div >
}
let showAccountPopoverIndex = 0
function HomeWatu() {
    const tableRef = useRef<{
        reload: Function
    }>()
    const pageStore = PageStore.useContainer()
    const userStore = UserStore.useContainer()
    const [showGroupModal, setShowGroupModal] = useState<boolean>(false)
    const [showGroupPriceModal, setShowGroupPriceModal] = useState<boolean>(false)
    const [showWatuGroupSettingModal, setShowWatuGroupSettingModal] = useState<boolean>(false)
    const [watuGroup, setWatuGroup] = useState<TWatuGroup>()
    const [showAccountPopover, setShowAccountPopover] = useState<boolean>(false)
    const [showRoleMonitorPage, setShowRoleMonitorPage] = useState<boolean>(false)
    const [roleMonitorData, setRoleMonitorData] = useState<any>({})
    const [formRef] = useForm()
    const [roleMonitor, setRoleMonitor] = useState<any>({})
    const { list: gameRoleList, reload } = usePage({
        isScroll: false,
        url: '/api/game_role/get_game_role_page',
        pageSize: 100,
        query: {
        }
    })
    const watuRoles = gameRoleList.filter((item: TGameRole) => item.groupId == watuGroup?.id)

    const updateStatus = (t: TGameRole) => {
        request({
            url: '/api/game_role/update_game_role',
            data: t,
            method: "post"
        }).then(res => {
            if (res.status == 0) {
                message.success('修改成功')
                setTimeout(() => {
                    reload()
                }, 500)
            }
        })
    }

    const getRoleMonitor = () => {
        request({
            url: '/api/report/get_role_baotu_monitor',
            data: {},
            method: "post"
        }).then(res => {
            if (res.status == 0) {
                const data: any = {}
                res.list.forEach((item: any) => {
                    data[item.gameId] = item
                })
                setRoleMonitor(data)
            }
        })
    }

    useEffect(() => {
        getRoleMonitor()
    }, [showGroupModal])

    const addContent = (work: string) => {
        const accounts = watuGroup?.gameServer ? pageStore.accountList.filter((item: TGameAccount) => { return item.gameServer == watuGroup?.gameServer }) : pageStore.accountList
        const options = accounts.map((item: TGameAccount) => {
            return { label: item.name, value: item.id }
        })
        return <div>
            <ChForm form={formRef} formData={[{
                label: '选择账号',
                name: 'accountIds',
                type: FormItemType.other,
                // @ts-ignore
                options: options,
                dom: <Select
                    mode="multiple"
                    options={options}
                    showSearch
                    optionFilterProp="label"
                />
            }]} />
            <Button onClick={() => {
                formRef.validateFields().then((res: any) => {
                    console.log(res.accountIds)
                    if (res.accountIds) {
                        let accounts = res.accountIds.map((id: any) => {
                            return pageStore.accountMap[id]
                        })
                        let gameServer = watuGroup?.gameServer
                        console.log('添加的账号为', accounts)
                        console.log('服务器为', gameServer)
                        console.log('工作内容', work)
                        request({
                            url: '/api/game_role/add_game_roles',
                            data: {
                                gameServer: gameServer,
                                work: work,
                                groupId: watuGroup?.id,
                                gameAccounts: accounts
                            },
                            method: "post"
                        }).then(res => {
                            if (res.status == 0) {
                                message.success('创建成功')
                                setShowAccountPopover(false)
                                setTimeout(() => {
                                    reload()
                                }, 1000)
                            } else {
                                message.error(res.message)
                            }
                        })
                    }

                })

            }} className="m-t-15" size="small" type="primary">确定</Button>
        </div>
    }
    const roleTag = (item: TGameRole) => {
        return <Popover trigger="click" placement="topLeft" title='操作' content={
            <div>
                <div style={{ marginLeft: 15 }}>id: {item.gameId};  </div>
                <div style={{ marginLeft: 15 }}>账号:{pageStore.accountMap[item.accoutId] && pageStore.accountMap[item.accoutId].username}</div>
                <div><Button onClick={() => { updateStatus(Object.assign({}, item, { status: '空闲' })) }} type="link">设置空闲</Button></div>
                <div><Button onClick={() => { updateStatus(Object.assign({}, item, { status: '忙碌' })) }} type="link">设置忙碌</Button></div>
                <div><Button onClick={() => { updateStatus(Object.assign({}, item, { status: '离线' })) }} type="link">设置离线</Button></div>
                <div><Button danger onClick={() => { updateStatus(Object.assign({}, item, { status: '删除' })) }} type="link">删除</Button></div>
            </div>
        }>
            <div style={{ margin: 5 }} className="flex-row-between">
                <Tag color="green">{item.name}{roleMonitor[item.gameId] && <span style={{ color: 'red' }}>-{roleMonitor[item.gameId] && roleMonitor[item.gameId].baotuCount}</span>}</Tag>
                {item.status == '离线' ? <div><Badge status="default" />离线</div> : item.status == '空闲' ? <div><Badge status="processing" />空闲</div> : <div><Badge status="warning" />忙碌</div>}
            </div>
        </Popover>
    }
    const getMonitorPageData = () => {
        request({
            url: '/api/report/get_role_baotu_monitor',
            data: {},
            method: "post"
        }).then(res => {
            if (res.status == 0) {
                let gameServerMap:any = {}
                res.list.forEach((item: any) => {
                    if(!gameServerMap[item.gameServer]) {
                        gameServerMap[item.gameServer] = [item]
                    }else {
                        gameServerMap[item.gameServer].push(item)
                    }
                })
                setRoleMonitorData(gameServerMap)
                setShowRoleMonitorPage(true)
            }
        })
    }
    return <div>
        <Modal title={"编辑分组货价 - " + watuGroup?.name} visible={showGroupPriceModal} onOk={() => {
            request({
                url: '/api/gameGroup/add_game_group',
                data: watuGroup,
                method: "post"
            }).then(res => {
                if (res.status == 0) {
                    message.success('修改成功')
                    setTimeout(() => {
                        reload()
                    }, 500)
                }
            })
        }} onCancel={() => {
            setShowGroupPriceModal(false)
        }}>
            <div className="flex">
                <div style={{ width: 100 }}>配置物价</div><TextArea rows={5} defaultValue={watuGroup?.priceConfig} onChange={(v) => {
                    watuGroup ? watuGroup.priceConfig = v.target.value : 0
                }} />
            </div>
        </Modal>
        <Modal title={"编辑分组角色 - " + watuGroup?.name}
            onOk={() => { setShowWatuGroupSettingModal(false) }}
            onCancel={() => setShowWatuGroupSettingModal(false)} visible={showWatuGroupSettingModal}>
            <div>
                <Button className="m-b-20" size="small" onClick={() => {
                    // tableRef.current!.reload()
                    reload()
                    getRoleMonitor()
                }}>刷新</Button>
                <div className="m-b-10 flex-row-center">
                    <h4>买图角色</h4>
                </div>
                <Row>
                    {watuRoles.filter((item: TGameRole) => item.work == '买图').map((item: TGameRole) => {
                        return <Col key={item.id} span={12}>
                            {roleTag(item)}
                        </Col>
                    })}
                </Row>
                <Popover onVisibleChange={(v) => {
                    if (v) {
                        formRef.resetFields()
                    }
                    setShowAccountPopover(v)
                    showAccountPopoverIndex = 1
                }
                } visible={showAccountPopover && showAccountPopoverIndex == 1} trigger="click" placement="topLeft" title='添加角色' content={addContent('买图')}>
                    <Button className="m-t-15" size="small">+添加角色</Button>
                </Popover>
            </div>
            <Divider />
            <div>
                <div className="m-b-10 flex-row-center">
                    <h4>发图角色</h4>
                </div>
                <Row>
                    {watuRoles.filter((item: TGameRole) => item.work == '发图').map((item: TGameRole) => {
                        return <Col key={item.id} span={12}>
                            {roleTag(item)}
                        </Col>
                    })}
                </Row>
                <Popover onVisibleChange={(v) => {
                    if (v) {
                        formRef.resetFields()
                    }
                    setShowAccountPopover(v)
                    showAccountPopoverIndex = 2
                }
                } visible={showAccountPopover && showAccountPopoverIndex == 2} trigger="click" placement="topLeft" title='添加角色' content={addContent('发图')}>
                    <Button className="m-t-15" size="small">+添加角色</Button>
                </Popover>
            </div>
            <Divider />
            <div>
                <div className="m-b-10 flex-row-center">
                    <h4>挖图角色</h4>
                </div>
                <Row>
                    {watuRoles.filter((item: TGameRole) => item.work == '挖图').map((item: TGameRole) => {
                        return <Col key={item.id} span={12}>
                            {roleTag(item)}
                        </Col>
                    })}
                </Row>
                <Popover onVisibleChange={(v) => {
                    if (v) {
                        formRef.resetFields()
                    }
                    showAccountPopoverIndex = 3
                    setShowAccountPopover(v)
                }
                } visible={showAccountPopover && showAccountPopoverIndex == 3} trigger="click" placement="topLeft" title='添加角色' content={addContent('挖图')}>
                    <Button className="m-t-15" size="small">+添加角色</Button>
                </Popover>
            </div>
            <Divider />
            <div>
                <div className="m-b-10 flex-row-center">
                    <h4>接货角色</h4>
                </div>
                <Row>
                    {watuRoles.filter((item: TGameRole) => item.work == '接货').map((item: TGameRole) => {
                        return <Col key={item.id} span={12}>
                            {roleTag(item)}
                        </Col>
                    })}
                </Row>
                <Popover onVisibleChange={(v) => {
                    if (v) {
                        formRef.resetFields()
                    }
                    showAccountPopoverIndex = 4
                    setShowAccountPopover(v)
                }
                } visible={showAccountPopover && showAccountPopoverIndex == 4} trigger="click" placement="topLeft" title='添加角色' content={addContent('接货')}>
                    <Button className="m-t-15" size="small">+添加角色</Button>
                </Popover>
            </div>
            <Divider />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分铁</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分铁').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 5
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 5} trigger="click" placement="topLeft" title='添加角色' content={addContent('分铁')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分铁50</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分铁50').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 50
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 50} trigger="click" placement="topLeft" title='添加角色' content={addContent('分铁50')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分铁60</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分铁60').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 60
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 60} trigger="click" placement="topLeft" title='添加角色' content={addContent('分铁60')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分铁70</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分铁70').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 70
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 70} trigger="click" placement="topLeft" title='添加角色' content={addContent('分铁70')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <Divider />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分书角色</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分书').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 6
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 6} trigger="click" placement="topLeft" title='添加角色' content={addContent('分书')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分书60</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分书60').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 61
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 61} trigger="click" placement="topLeft" title='添加角色' content={addContent('分书60')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分书70</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分书70').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 62
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 62} trigger="click" placement="topLeft" title='添加角色' content={addContent('分书70')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <Divider />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分兽内角色</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分兽决内丹').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 7
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 7} trigger="click" placement="topLeft" title='添加角色' content={addContent('分兽决内丹')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <Divider />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分环</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分环').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 8
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 8} trigger="click" placement="topLeft" title='添加角色' content={addContent('分环')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分环50</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分环50').map((item: TGameRole) => {
                                return <Col key={item.id} span={12}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 80
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 80} trigger="click" placement="topLeft" title='添加角色' content={addContent('分环50')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <br />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分环60</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分环60').map((item: TGameRole) => {
                                return <Col key={item.id} span={12}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 81
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 81} trigger="click" placement="topLeft" title='添加角色' content={addContent('分环60')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分环70</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分环70').map((item: TGameRole) => {
                                return <Col key={item.id} span={12}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 82
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 82} trigger="click" placement="topLeft" title='添加角色' content={addContent('分环70')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <Divider />
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分五宝角色</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分五宝').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 9
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 9} trigger="click" placement="topLeft" title='添加角色' content={addContent('分五宝')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>分杂货</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '分杂货').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 10
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 10} trigger="click" placement="topLeft" title='添加角色' content={addContent('分杂货')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
            <Row>
                <Col span={12}>
                    <div>
                        <div className="m-t-10 flex-row-center">
                            <h4>后勤</h4>
                        </div>
                        <Row>
                            {watuRoles.filter((item: TGameRole) => item.work == '后勤').map((item: TGameRole) => {
                                return <Col key={item.id}>
                                    {roleTag(item)}
                                </Col>
                            })}
                        </Row>
                        <Popover onVisibleChange={(v) => {
                            if (v) {
                                formRef.resetFields()
                            }
                            showAccountPopoverIndex = 101
                            setShowAccountPopover(v)
                        }
                        } visible={showAccountPopover && showAccountPopoverIndex == 101} trigger="click" placement="topLeft" title='添加角色' content={addContent('后勤')}>
                            <Button className="m-t-15" size="small">+添加角色</Button>
                        </Popover>
                    </div>
                </Col>
            </Row>
        </Modal>
        <Modal visible={showGroupModal} onCancel={() => { setShowGroupModal(false) }} onOk={() => {
            const id = userStore.user?.id
            formRef.validateFields().then((res) => {
                request({
                    url: '/api/gameGroup/add_game_group',
                    data: {
                        name: res.name,
                        type: '挖图组',
                        gameServer: res.gameServer,
                        userId: id,
                    },
                    method: "post"
                }).then(res => {
                    message.success('创建成功')
                    tableRef.current!.reload()
                    setShowGroupModal(false)
                })

            })
        }} >
            <ChForm form={formRef} formData={[{
                label: '分组名称',
                name: 'name',
                type: FormItemType.input,
            }, {
                label: '分组服务器',
                name: 'gameServer',
                type: FormItemType.input,
            }
            ]} />
        </Modal>
        <Modal onCancel={()=>setShowRoleMonitorPage(false)} footer={false} visible={showRoleMonitorPage}>
            <h4>挖图监控</h4>
            <Button size="small" onClick={()=>getMonitorPageData()}>刷新</Button>
            {
                Object.keys(roleMonitorData).map(gameServer=>{
                    return <div key={gameServer}>
                        <div>{gameServer}</div>
                        {
                            roleMonitorData[gameServer].map((item:any)=>{
                                let isRed = false
                                if(item.work === '发图' && item.amount < 80) {
                                    isRed = true
                                }
                                if(item.work === '挖图' && item.amount > 250) {
                                    isRed = true
                                }
                                if(item.work === '接货' && item.amount > 20) {
                                    isRed = true
                                }
                                return <div style={{color: `${isRed?'red':'#333'}`}} key={item.gameId}>
                                    <span>【{item.work}】</span>
                                    <span>{item.name}</span>
                                    <span>{item.amount}</span>
                                </div>
                            })
                        }
                    </div>
                })
            }
        </Modal>
        <Collapse defaultActiveKey={['1']}>
            <Panel header="挖图功能" key="1">
                <Row>
                    <Col><div style={{ 'marginLeft': '10px' }}>挖图配置:</div></Col>
                    <Col>
                        <Select size="small" style={{ marginLeft: 5 }} placeholder='请选择仓库位置' defaultValue={pageStore.cangkuPath} onChange={(v) => {
                            // @ts-ignore
                            window.cangkuPath = v; pageStore.setCangkuPath(v)
                        }}>
                            <Select.Option value="长安城">长安城</Select.Option>
                            <Select.Option value="建邺城">建邺城</Select.Option>
                        </Select>
                    </Col>
                    <Col>
                        <div style={{ marginLeft: 20 }}>
                            <span style={{ color: '#000' }}>补蓝</span>： <Switch size="small" checked={pageStore.isChilan} onChange={(e) => {
                                pageStore.handleChangeIsChilan(e)
                                // pageStore.handleChangeIsBeen(e);
                            }} />
                        </div>
                    </Col>
                    {/* <Col>
                        <div style={{ marginLeft: 20 }}>
                            <span style={{ color: '#000' }}>联动模式</span>： <Switch size="small" onChange={(e) => {
                                pageStore.handleChangeIsBeen(e);
                            }} />
                        </div>
                    </Col> */}
                </Row>
                <br />
                <Row>
                    <Col>
                        <Button onClick={() => {
                            pageStore.handleGetWatuInfo()
                        }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12 m-l-10'>开始挖图</Button>
                    </Col>
                    <Col>
                        <Button onClick={() => {
                            pageStore.handleGetWatuInfo(1)
                        }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12 m-l-10'>重新扫描</Button>
                    </Col>
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.sellEquipment() }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>卖装备</Button>
                    </Col>
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.throwLitter() }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>丢垃圾</Button>
                    </Col>
                </Row>
                <br />
                <div className="home-feature-panel">
                    {pageStore.watuInfo && <ChMhMapTool cangkuPath={pageStore.cangkuPath} deviceId={watuDeviceId} mapName={pageStore.watuInfo.mapName} points={pageStore.watuInfo.points}></ChMhMapTool>}
                </div>
                <br />
            </Panel>
            <Panel header={"挖图组配置"} key="2">
                <Button className="m-b-10" size="small" type="primary" onClick={() => { setShowGroupModal(true) }}> 添加分组 </Button>
                <Button onClick={()=>getMonitorPageData()} className="m-b-10 m-l-10" size="small" type="primary"> 角色监控 </Button>
                <ChTablePanel
                    ref={tableRef}
                    disablePagination={true}
                    formData={[]}
                    url="/api/gameGroup/get_game_group_page?type='挖图组'"
                    columns={[
                        {
                            title: '分组编码',
                            dataIndex: 'id',
                            key: 'id',
                        },
                        {
                            title: '名称',
                            dataIndex: 'name',
                            key: 'name',
                        },
                        {
                            title: '服务器',
                            dataIndex: 'gameServer',
                            key: 'gameServer',
                        }, {
                            title: '操作',
                            dataIndex: 'option',
                            key: 'option',
                            render: (_: any, item: TWatuGroup) => {
                                return <div className="flex" style={{ width: '120px' }}>
                                    <Button onClick={() => {
                                        setWatuGroup(item)
                                        setShowWatuGroupSettingModal(true)
                                    }} type="link">配置角色</Button>
                                    <Button onClick={() => {
                                        setWatuGroup(item)
                                        setShowGroupPriceModal(true)
                                    }} type="link">分组货价</Button>
                                </div>
                            }
                        }
                    ]}
                />
            </Panel>
        </Collapse>
    </div >
}
function HomeFeature() {
    const [price, setPrice] = useState('25555')
    const userStore = UserStore.useContainer()
    const pageStore = PageStore.useContainer()
    return !pageStore.lock ? <div></div> : <div className='home-feature'>
        <Button type="primary" icon={<CloseCircleOutlined />} className='fs-12 m-r-5' size="small" onClick={() => {
            const id = userStore.user?.id
            if (id && id != 1) {

                confirm({
                    title: '更新后无法复原',
                    content: 'Some descriptions',
                    onOk() {
                        doUpdatePy();
                        message.success('更新成功，请不要重复更新')

                    },
                    onCancel() {
                        console.log('Cancel');
                    },
                });
            } else {
                confirm({
                    title: '开发者是否确认更新',
                    content: 'Some descriptions',
                    onOk() {
                        doUpdatePy();
                        console.log('OK');
                    },
                    onCancel() {
                        console.log('Cancel');
                    },
                });
            }
            pageStore.setShowLog(true)
        }}>更新脚本</Button>
        <Button type="primary" icon={<CloseCircleOutlined />} className='fs-12 m-l-5' size="small" onClick={() => { pageStore.closeAllTask() }}>关闭全部脚本</Button>
        <Tabs onChange={(v) => pageStore.setFeatureTabIndex(v)} type="card" defaultActiveKey={pageStore.featureTabIndex} style={{ marginBottom: 32 }}>
            <TabPane tab="通用功能" key="1">
                <Row className="m-b-20">
                    <Col>
                        <span style={{ color: '#000' }}>开启硬件驱动</span>： <Switch size="small" checked={pageStore.isYinjian} onChange={(e) => {
                            pageStore.handleChangeIsYinjian(e)
                            // pageStore.handleChangeIsBeen(e);
                        }} />
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Button type='primary' onClick={() => { pageStore.handleTest() }} loading={pageStore.getTaskLoading('test')} icon={<ToolOutlined />} size='small' className='fs-12'>测试脚本</Button>
                    </Col>
                    
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.connector() }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>连点器</Button>
                    </Col>
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.setsShowHanhu(true) }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>自动喊话</Button>
                    </Col>
                </Row>
            </TabPane>
            <TabPane tab="挖图" key="2">
                <HomeWatu />
            </TabPane>
            {userStore.user.vipCard.level > 0 && <TabPane tab="抓鬼" key="4">
                <Row>
                    <Col>
                        <Button onClick={() => {
                            pageStore.setShowLog(true)
                            message.success('操作成功')
                            pageStore.doTaskAuth(() => {
                                doZhuaGuiTask(pageStore.isBigGhost ? 1 : 0)
                            })
                        }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>自动抓鬼</Button>
                    </Col>
                    <Col offset={1}>
                        是否抓大鬼&nbsp;&nbsp;
                        <Switch size="small" checked={pageStore.isBigGhost} onChange={(e) => {
                            pageStore.setIsBigGhost(e)
                        }} />
                    </Col>
                </Row>
            </TabPane>
            }
            {
                userStore.user.vipCard.level == 100 && <TabPane tab="补店" key="5">
                    <Row>
                        <Col>
                            <Button onClick={() => {
                                pageStore.setShowLog(true)
                                message.success('操作成功')
                                doBudianTask(price)
                            }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>自动抓律法女娲</Button></Col>
                        <Col offset={1}> <span>价格：</span><Input onChange={(e) => { setPrice(e.target.value) }} value={price} style={{ width: 150 }} /></Col>

                    </Row>
                </TabPane>}
        </Tabs>

        <Modal visible={pageStore.isShowHanhu} onCancel={() => { pageStore.setsShowHanhu(false) }} onOk={() => {
            pageStore.hanghua()
            pageStore.setsShowHanhu(false)
        }} >
            <div>请输入喊话个数 <Input onChange={
                // @ts-ignore
                v => window.hanghuaCount = v.target.value
            } />
            </div>
        </Modal>
    </div>

}
function Home() {
    // @ts-ignore
    return <div className='flex home-page page'>
        <ModalMultipleAccountSelect />
        <HomeGameArea />
        <HomeFeature />
    </div>
}
export default Home
