import React, {useState} from "react";
import {Button, Col, message, Modal, Row} from 'antd'
import {TDevice} from "../../typing";
import "./index.less";
import {ChForm, ChUtils, FormItemType} from "ch-ui";
import {useForm} from "antd/es/form/Form";
import {doStartGame, doTest, getJiangjunCode} from "../../call";
import {
    ScanOutlined,
    InsertRowBelowOutlined,
    CloseCircleOutlined,
    ToolOutlined
} from '@ant-design/icons';

type TPanelTask = 'test' | 'login' | ''

const { useOptionFormListHook } = ChUtils.chHooks

function usePageStore() {
    const [formRef] = useForm()
    const [isTasking, setIsTasking] = useState<boolean>(false)
    const [currentTask, setCurrentTask] = useState<TPanelTask>('')
    const [code, setCode] = useState<number>()
    const [linkDeviceId, setLinkDeviceId] = useState<number|undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const {optionsMap: deviceMap, options: deviceOptions} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}})
    const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    const handleClickPreviewDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=192.168.8.120&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=${device.ip}&port=5900&resize=scale&autoconnect=true&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
        setTimeout(()=>{
            // @ts-ignore
            window.document.querySelector('.home-device-body').scrollTop = 64
        }, 1000)
    }
    const logAllAccount = (type: number) => {
        message.success('启动成功')
        setTimeout(()=>{
            if(type === 1) {
                const ret = doStartGame(['ch.1993.com'])
                if(ret) {
                    // setCode(ret.code)
                }
            }
            if(type === 2) {
                const ret = doStartGame(['ch1993com1', 'ch1993com6', 'ch1993com7', 'ch1993com8', 'mm1042061794'])
                if(ret) {
                    // setCode(ret.code)
                }
            }
        }, 1000)
    }
    const handleSelectJiangjunDevice = () => {
        formRef.validateFields().then((res: any) => {
            if(res.deviceId) {
                const device: TDevice = deviceMap[res.deviceId]
                handleClickLinkDevice(device)
                setShowSelectDeviceModal(false)
                message.success('导入将军令中，请稍后...')
                setTimeout(()=>{
                    // const ret = getJiangjunCode({})
                    // if(ret && ret.code) {
                    //     setCode(ret.code)
                    // }
                }, 5000)
            }
        })
    }
    const handleTest = ()=>checkIsTasking(() => {
        setCurrentTask('test')
        setIsTasking(true)
        const res = doTest()
        if(res.status == 0) {
            message.success('连接成功')
            setIsTasking(false)
        }
    })
    const checkIsTasking = (cb: Function) => {
        if(!isTasking) {
            cb()
        }else {
            message.warn('当前有任务进行中')
        }
    }
    const getTaskLoading = (task: TPanelTask) => {
        return isTasking && task === currentTask
    }
    return {
        isTasking,
        logAllAccount,
        handleClickPreviewDevice,
        formRef,
        linkDeviceId,
        setLinkDeviceId,
        deviceOptions,
        handleClickLinkDevice,
        handleSelectJiangjunDevice,
        showSelectDeviceModal,
        setShowSelectDeviceModal,
        currentPhoneUrl,
        setCurrentPhoneUrl,
        code,
        handleTest,
        getTaskLoading
    }
}

function Home() {
    const pageStore = usePageStore()
    return <div className='flex home-page page'>
        <div className='login-game-area'>
            <div className='flex-row-center'>
                <div>
                    <div className='flex-row-center m-b-20'>
                        <Button icon={<ScanOutlined />} className='fs-12' size="small"  onClick={()=>{
                            pageStore.setShowSelectDeviceModal(true)
                        }}>导入将军令</Button>
                        <Button icon={<CloseCircleOutlined />} className='fs-12 m-l-5' size="small" onClick={()=>{pageStore.setCurrentPhoneUrl(''); message.success('关闭成功')}}>关闭连接</Button>
                        {/*<div>{pageStore.currentPhoneUrl}</div>*/}

                        {/*<Button className={'m-l-20'} type={"primary"} onClick={()=>{*/}
                        {/*    pageStore.logAllAccount(2)*/}
                        {/*}}>一件启动2号队伍</Button>*/}
                    </div>
                    <div className='home-device-preview'>
                        <div className='home-device-body'>
                            <iframe frameBorder={0} id='appBody' src={pageStore.currentPhoneUrl}/>
                        </div>
                    </div>
                    <div className='home-log-panel'>
                        <div>程序运行中,等待日志输入...</div>
                    </div>
                </div>
            </div>
            <Modal onCancel={()=>pageStore.setShowSelectDeviceModal(false)} onOk={()=>pageStore.handleSelectJiangjunDevice()} visible={pageStore.showSelectDeviceModal}>
                <div>
                    <ChForm form={pageStore.formRef} formData={[{ type: FormItemType.select, label: '选择设备', name: 'deviceId', options: pageStore.deviceOptions}]}/>
                </div>
            </Modal>
        </div>
        <div className='home-feature'>
            <Row>
                <Col>
                    <Button type='primary' onClick={()=>{ pageStore.handleTest() }} loading={pageStore.getTaskLoading('test')} icon={<ToolOutlined />} size='small' className='fs-12'>测试脚本</Button>
                </Col>
                <Col>
                    <Button onClick={()=>{pageStore.logAllAccount(1)}} icon={<InsertRowBelowOutlined />} type='primary' size='small' className='fs-12 m-l-10'>一键起号</Button>
                </Col>
            </Row>

        </div>
    </div>
}

export default Home
