import React, { useEffect, useState, useRef } from "react";
import { Button, Col, Input, message, Modal, Popover, Row, Select, Switch, Tabs, Collapse, Divider, Badge, Tag} from 'antd'
import { TDevice, TGameAccount, TGameRole, TWatuGroup } from "../../typing";
import "./index.less";
const request = ChUtils.Ajax.request
import { ChForm, ChTablePanel, ChUtils, FormItemType } from "ch-ui";
import { useForm } from "antd/es/form/Form";
import { doKillProcess, doStartGame, doTest, doTest2, MainThread, doGetWatuInfo, doZhuaGuiTask, doBee, doGetWatuClickMap, doCloseAllTask, doThrowLitter, doSellEquipment, doConnector, doZhandou, doHanghua } from "../../call";
import { createContainer } from 'unstated-next'
const { TabPane } = Tabs;
const { Panel } = Collapse;
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

type TPanelTask = 'test' | 'test2' | 'login' | ''
const { useOptionFormListHook, usePage } = ChUtils.chHooks

type TWatuInfo = {
    mapName: string,
    points: [number, number][]
    deviceId?: number
}

let selectDeviceFunc: 'handleSelectJiangjunDevice' | 'handleSelectWatuDevice' | 'handleSelectZhuaGuiDevice'
let watuDeviceId = 0
let zhuaGuiDeviceId = 0
export function usePageStore() {
    useEffect(() => {
        MainThread.messageListener.pushLogHandles = [handlePushLog]
        MainThread.messageListener.pushStateHandles = [handlePushState]
        MainThread.messageListener.methodGetWatuInfoReplyHandles = [handleGetWatuInfoReply]
        // @ts-ignore
        window.cangkuPath = '长安城'
    }, [])
    const [logs, setLogs] = useState<string[]>([])
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
    const [cangkuPath, setCangkuPath] = useState<string>('长安城');
    const [currentTask, setCurrentTask] = useState<TPanelTask>('')
    const [code, setCode] = useState<number>()
    const [watuInfo, setWatuInfo] = useState<TWatuInfo>()
    const [linkDeviceId, setLinkDeviceId] = useState<number | undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const { optionsMap: deviceMap, options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {} })
    const { optionsMap: accountMap, options: accountOptions, list: accountList } = useOptionFormListHook({ url: '/api/game_account/get_game_account_options', query: {} })
    const handlePushLog = (log: string) => { setLogs((logs) => [...logs, log]) }
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
    const handleGetWatuInfo = (deviceId: number, acceptId: string) => {
        if (isBee) {
            doBee(deviceId, cangkuPath, acceptId)
        } else {
            doGetWatuInfo(deviceId, cangkuPath, acceptId)
        }
    }
    const closeAllTask = () => {
        message.success('操作成功');
        doCloseAllTask()
    }
    const throwLitter = () => {
        message.success('操作成功');
        doThrowLitter(watuDeviceId)
    }
    const sellEquipment = () => {
        message.success('操作成功');
        doSellEquipment(watuDeviceId)
    }
    const handleGetWatuInfoReply = (data: any) => {
        console.log('handleGetWatuInfoReply', data);
        const result = data.result
        const mapName = result[0][0] || result[1][0] || result[2][0]
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
            setTimeout(() => {
                console.log('直接开始挖图');
                // @ts-ignore
                if (window.isBee) {
                    // @ts-ignore
                    doGetWatuClickMap(...window.beeData, true, window.cangkuPath, window.acceptId)
                }
            }, 1000)
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
    const handleSelectWatuDevice = () => {
        formRef.validateFields().then((res: any) => {
            if (res.deviceId) {
                if (res.acceptId) {
                    // @ts-ignore
                    window.acceptId = res.acceptId
                }
                watuDeviceId = res.deviceId
                handleGetWatuInfo(res.deviceId, res.acceptId)
                setShowSelectDeviceModal(false)
            }
        })
    }
    const handleSelectZhuaGuiDevice = () => {
        formRef.validateFields().then((res: any) => {
            if (res.deviceId) {
                zhuaGuiDeviceId = res.deviceId
                doZhuaGuiTask(res.deviceId)
                setShowSelectDeviceModal(false)
            }
        })
    }
    const handleTest = () => checkIsTasking(() => {
        setCurrentTask('test')
        setIsTasking(true)
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
    const connector = () => {
        message.success('操作成功')
        if (watuDeviceId > 0) {
            doConnector(watuDeviceId)
        }

    }
    const zhandou = () => {
        message.success('操作成功')
        doZhandou(watuDeviceId)
    }
    const hanghua = () => {
        message.success('操作成功')
        // @ts-ignore
        doHanghua(window.hanghuaCount)
    }
    const 弹出添加分组框 = () => {
        alert('添加分组')
    }
    return {
        弹出添加分组框,
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
        handleSelectWatuDevice,
        handleSelectZhuaGuiDevice,
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
            pageStore.handleSelectWatuDevice()
        } else if (selectDeviceFunc === 'handleSelectZhuaGuiDevice') {
            pageStore.handleSelectZhuaGuiDevice()
        }

    }
    const runningPyProcess = pageStore.processState.runningPyProcess || {}
    return <div className='login-game-area'>
        <div className='flex-row-center'>
            <div>
                <div className='flex-row-center m-b-20'>
                    <Button icon={<ScanOutlined />} className='fs-12' size="small" onClick={() => {
                        selectDeviceFunc = 'handleSelectJiangjunDevice'
                        pageStore.setShowSelectDeviceModal(true)
                    }}>导入将军令</Button>
                    <Button icon={<CloseCircleOutlined />} className='fs-12 m-l-5' size="small" onClick={() => { pageStore.setCurrentPhoneUrl(''); message.success('关闭成功') }}>关闭连接</Button>
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
                <div className='home-log-panel'>
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
            </div>
        </div>
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
    </div>
}

let showAccountPopoverIndex = 0
function HomeWatu() {
    const tableRef = useRef<{
        reload: Function
    }>()
    const pageStore = PageStore.useContainer()
    const userStore = UserStore.useContainer()
    const [showGroupModal, setShowGroupModal] = useState<boolean>(false)
    const [showWatuGroupSettingModal, setShowWatuGroupSettingModal] = useState<boolean>(false)
    const [watuGroup, setWatuGroup] = useState<TWatuGroup>()
    const [showAccountPopover, setShowAccountPopover] = useState<boolean>(false)
    const [formRef] = useForm()
    const { list: gameRoleList, reload } = usePage({
        isScroll: false,
        url: '/api/game_role/get_game_role_page',
        pageSize: 100,
        query: {
        }
    })
    const watuRoles = gameRoleList.filter((item: TGameRole)=>item.groupId == watuGroup?.id)

    const updateStatus = (t: TGameRole) => {
        request({
            url: '/api/game_role/update_game_role',
            data: t,
            method: "post"
        }).then(res => {
            if (res.status == 0) {
                message.success('修改成功')
                setTimeout(()=>{
                    reload()
                }, 500)
            }
        })
    }

    const addContent = (work: string) => {
        const accounts = watuGroup?.gameServer ? pageStore.accountList.filter((item: TGameAccount)=>{return item.gameServer == watuGroup?.gameServer}): pageStore.accountList
        const options = accounts.map((item: TGameAccount)=>{
            return {label: item.name, value: item.id}
        })
       return <div>
        <ChForm form={formRef} formData={[{
            label: '选择账号',
            name: 'accountIds',
            type: FormItemType.multipleSelect,
            // @ts-ignore
            options: options,
        }]} />
        <Button onClick={() => {
            formRef.validateFields().then((res: any) => {
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
                            setTimeout(()=>{
                                reload()
                            }, 1000)
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
                <div><Button onClick={()=>{ updateStatus(Object.assign({},item, {status: '空闲'})) }} type="link">设置空闲</Button></div>
                <div><Button onClick={()=>{ updateStatus(Object.assign({},item, {status: '忙碌'})) }} type="link">设置忙碌</Button></div>
                <div><Button onClick={()=>{ updateStatus(Object.assign({},item, {status: '离线'})) }} type="link">设置离线</Button></div>
                <div><Button danger onClick={()=>{ updateStatus(Object.assign({},item, {status: '删除'})) }} type="link">删除</Button></div>
            </div>
        }>
            <div style={{ width: 120, margin: 5 }} className="flex-row-between">
            <Tag color="green">{item.name}</Tag>
            {item.status == '离线' ?<div><Badge status="default" />离线</div> : item.status == '空闲' ?<div><Badge status="processing" />空闲</div>: <div><Badge status="warning" />忙碌</div>}
        </div>
        </Popover>
    }
    return <div>
        <Modal title={"编辑分组角色 - " + watuGroup?.name}
            onOk={() => { setShowWatuGroupSettingModal(false) }}
            onCancel={() => setShowWatuGroupSettingModal(false)} visible={showWatuGroupSettingModal}>
            <div>
                <Button className="m-b-20" size="small" onClick={()=>{
                    // tableRef.current!.reload()
                    reload()
                }}>刷新</Button>
                <div className="m-b-10 flex-row-center">
                    <h4>买图角色</h4>
                </div>
                <Row>
                    {watuRoles.filter((item: TGameRole)=>item.work == '买图').map((item:TGameRole) => {
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
                    {watuRoles.filter((item: TGameRole)=>item.work == '发图').map((item:TGameRole) => {
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
                    {watuRoles.filter((item: TGameRole)=>item.work == '挖图').map((item:TGameRole) => {
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
                    {watuRoles.filter((item: TGameRole)=>item.work == '接货').map((item:TGameRole) => {
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
        <Collapse defaultActiveKey={['1', '2']}>
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
                            <span style={{ color: '#000' }}>小蜜蜂模式</span>： <Switch size="small" checked={pageStore.isBee} onChange={(e) => {
                                pageStore.handleChangeIsBeen(e);
                            }} />
                        </div>
                    </Col>
                </Row>
                <br />
                <Row>
                    <Col>
                        <Button onClick={() => {
                            selectDeviceFunc = 'handleSelectWatuDevice'
                            pageStore.setShowSelectDeviceModal(true)
                        }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12 m-l-10'>开始挖图</Button>
                    </Col>
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.sellEquipment() }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>卖装备</Button>
                    </Col>
                    <Col className="m-l-10">
                        <Button onClick={() => { pageStore.throwLitter() }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>丢垃圾</Button>
                    </Col>
                </Row>
                <br />
                <br />
                <br />
            </Panel>
            <Panel header={"挖图组配置"} key="2">
                <Button className="m-b-10" size="small" type="primary" onClick={() => { setShowGroupModal(true) }}> 添加分组 </Button>

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
                            title: '分组类型',
                            dataIndex: 'type',
                            key: 'type',
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
                                return <div style={{ width: '120px' }}>
                                    <Button onClick={() => {
                                        setWatuGroup(item)
                                        setShowWatuGroupSettingModal(true)
                                    }} type="link">配置角色</Button>
                                </div>
                            }
                        }
                    ]}
                />
            </Panel>
        </Collapse>
    </div>
}
function HomeFeature() {
    const pageStore = PageStore.useContainer()
    return <div className='home-feature'>
        <div></div>
        <Tabs onChange={(v) => pageStore.setFeatureTabIndex(v)} type="card" defaultActiveKey={pageStore.featureTabIndex} style={{ marginBottom: 32 }}>
            <TabPane tab="通用功能" key="1">
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
            <TabPane tab="抓鬼" key="4">
                <Row>
                    <Col>
                        <Button onClick={() => {
                            selectDeviceFunc = 'handleSelectZhuaGuiDevice'
                            pageStore.setShowSelectDeviceModal(true)
                        }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12'>自动抓鬼</Button>
                    </Col>
                </Row>
            </TabPane>
            <TabPane tab="其他" key="5">
                <Row>

                </Row>
            </TabPane>

        </Tabs>
        <div className="home-feature-panel">
            {pageStore.watuInfo && <ChMhMapTool cangkuPath={pageStore.cangkuPath} deviceId={watuDeviceId} mapName={pageStore.watuInfo.mapName} points={pageStore.watuInfo.points}></ChMhMapTool>}
        </div>
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
