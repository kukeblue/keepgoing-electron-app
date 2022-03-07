import React, {useState} from "react";
import {Button, Col, message, Modal, Row} from 'antd'
import {TDevice} from "../../typing";
import "./index.less";
import {ChForm, ChUtils, FormItemType} from "ch-ui";
import {useForm} from "antd/es/form/Form";
import {doStartGame, getJiangjunCode} from "../../call";
const { useOptionFormListHook } = ChUtils.chHooks

function usePageStore() {
    const [formRef] = useForm()
    const [code, setCode] = useState<number>()
    const [linkDeviceId, setLinkDeviceId] = useState<number|undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const {optionsMap: deviceMap, options: deviceOptions} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}})
    const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    const handleClickPreviewDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=192.168.8.120&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        setCurrentPhoneUrl(owurl)
    }
    const logAllAccount = (type: number) => {
        setTimeout(()=>{
            if(type === 1) {
                const ret = doStartGame(['ch.1993.com', 'ch1993com2', 'ch1993com3', 'ch1993com4', 'ch1993com5'])
                if(ret && ret.code) {
                    setCode(ret.code)
                }
            }
            if(type === 1) {
                const ret = doStartGame(['ch1993com1', 'ch1993com6', 'ch1993com7', 'ch1993com8', 'mm1042061794'])
                if(ret && ret.code) {
                    setCode(ret.code)
                }
            }

        }, 5000)
    }
    const handleSelectJiangjunDevice = () => {
        formRef.validateFields().then((res: any) => {
            if(res.deviceId) {
                const device: TDevice = deviceMap[res.deviceId]
                handleClickLinkDevice(device)
                setShowSelectDeviceModal(false)
                setTimeout(()=>{
                    const ret = getJiangjunCode({})
                    if(ret && ret.code) {
                        setCode(ret.code)
                    }
                }, 5000)
            }
        })
    }

    return {
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
        code
    }
}

function Home() {
    const pageStore = usePageStore()
    return <div className='flex home-page page'>
        <div className='login-game-area'>
            <div className='flex-row-center'>
                <div>
                    <div className='flex-row-center m-b-20'>
                        <Button  type={"primary"} onClick={()=>{
                            pageStore.setShowSelectDeviceModal(true)
                        }}>获取将军令</Button>
                        <Button className={'m-l-20'} type={"primary"} onClick={()=>{
                            pageStore.logAllAccount(1)
                        }}>一件启动1号队伍</Button>
                        <Button className={'m-l-20'} type={"primary"} onClick={()=>{
                            pageStore.logAllAccount(2)
                        }}>一件启动2号队伍</Button>
                    </div>
                    <div className='home-device-preview'>
                        <div className='home-device-body'>
                            <iframe frameBorder={0} id='appBody' width='100%' height='100%' src={pageStore.currentPhoneUrl}/>
                        </div>
                        <Button  onClick={()=>{pageStore.setCurrentPhoneUrl(''); message.success('关闭成功')}} className='m-t-20'>关闭将军手机连接</Button>
                        <div>{pageStore.currentPhoneUrl}</div>
                    </div>
                </div>
            </div>
            <Modal onCancel={()=>pageStore.setShowSelectDeviceModal(false)} onOk={()=>pageStore.handleSelectJiangjunDevice()} visible={pageStore.showSelectDeviceModal}>
                <div>
                    <ChForm form={pageStore.formRef} formData={[{ type: FormItemType.select, label: '选择设备', name: 'deviceId', options: pageStore.deviceOptions}]}/>
                </div>
            </Modal>
        </div>
        <div className='home-feature'></div>
    </div>
}

export default Home
