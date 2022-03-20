import React, { useEffect, useState } from "react";
import { Button, Col, message, Modal, Popover, Row } from 'antd'
import { TDevice } from "../../typing";
import "./index.less";
import { ChForm, ChUtils, FormItemType } from "ch-ui";
import { useForm } from "antd/es/form/Form";
import { doKillProcess, doStartGame, doTest, doTest2, MainThread, doGetWatuInfo } from "../../call";
import { createContainer } from 'unstated-next'

import {
    DownCircleOutlined,
    ClearOutlined,
    CloseCircleOutlined,
    InsertRowBelowOutlined,
    ScanOutlined,
    SettingOutlined,
    ToolOutlined
} from '@ant-design/icons';
import ChMhMapTool from "../../components/ChMhMapTool";

type TPanelTask = 'test' | 'test2' | 'login' | ''
const { useOptionFormListHook } = ChUtils.chHooks

type TWatuInfo = {
    mapName: string,
    points: [number, number][]
}

let selectDeviceFunc: 'handleSelectJiangjunDevice' | 'handleSelectWatuDevice'

function usePageStore() {
    useEffect(() => {
        MainThread.messageListener.pushLogHandles.push(handlePushLog)
        MainThread.messageListener.pushStateHandles.push(handlePushState)
        MainThread.messageListener.methodGetWatuInfoReplyHandles.push(handleGetWatuInfoReply)
    }, [])
    const [logs, setLogs] = useState<string[]>([])
    const [processState, setProcessState] = useState({
        runningPyProcess: {}
    })
    const [formRef] = useForm()
    const [modalMultipleAccountSelectShow, setModalMultipleAccountSelectShow] = useState(false)
    const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    const [isTasking, setIsTasking] = useState<boolean>(false)
    const [currentTask, setCurrentTask] = useState<TPanelTask>('')
    const [code, setCode] = useState<number>()
    const [watuInfo, setWatuInfo] = useState<TWatuInfo>()
    const [linkDeviceId, setLinkDeviceId] = useState<number | undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const { optionsMap: deviceMap, options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {} })
    const { optionsMap: accountMap, options: accountOptions } = useOptionFormListHook({ url: '/api/game_account/get_game_account_options', query: {} })
    const handlePushLog = (log: string) => { setLogs((logs) => [...logs, log]) }
    const handlePushState = (processState: any) => { setProcessState(processState) }
    const handleClickPreviewDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=192.168.8.120&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=${device.ip}&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
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
    const handleGetWatuInfo = (deviceId: number) => {
        doGetWatuInfo(deviceId)
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
            points
        })
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
                handleGetWatuInfo(res.deviceId)
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
    return {
        setModalMultipleAccountSelectShow,
        modalMultipleAccountSelectShow,
        accountMap,
        accountOptions,
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
        handleGetWatuInfo
    }
}

export const PageStore = createContainer(usePageStore)

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
        } else {
            pageStore.handleSelectWatuDevice()
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
                <ChForm form={pageStore.formRef} formData={[{ type: FormItemType.select, label: '选择设备', name: 'deviceId', options: pageStore.deviceOptions }]} />
            </div>
        </Modal>
    </div>

}
function HomeFeature() {
    const pageStore = PageStore.useContainer()
    return <div className='home-feature'>
        <Row>
            <Col>
                <Button type='primary' onClick={() => { pageStore.handleTest() }} loading={pageStore.getTaskLoading('test')} icon={<ToolOutlined />} size='small' className='fs-12'>测试脚本</Button>
            </Col>
            <Col>
                <Button loading={pageStore.getTaskLoading('test2')} onClick={() => { pageStore.handleTest2() }} icon={<InsertRowBelowOutlined />} type='primary' size='small' className='fs-12 m-l-10'>异步测试脚本</Button>
            </Col>
            <Col>
                <Button onClick={() => {
                    pageStore.setModalMultipleAccountSelectShow(true)
                }} icon={<InsertRowBelowOutlined />} type='primary' size='small' className='fs-12 m-l-10'>一键起号</Button>
            </Col>
            <Col>
                <Button onClick={() => {
                    selectDeviceFunc = 'handleSelectWatuDevice'
                    pageStore.setShowSelectDeviceModal(true)
                }} icon={<DownCircleOutlined />} type='primary' size='small' className='fs-12 m-l-10'>挖图位置解析</Button>
            </Col>
        </Row>
        <div className="home-feature-panel">
            {pageStore.watuInfo && <ChMhMapTool mapName={pageStore.watuInfo.mapName} points={pageStore.watuInfo.points}></ChMhMapTool>}
        </div>
    </div>

}
function Home() {
    return <PageStore.Provider><div className='flex home-page page'>
        <ModalMultipleAccountSelect />
        <HomeGameArea />
        <HomeFeature />
    </div></PageStore.Provider>
}

export default Home
