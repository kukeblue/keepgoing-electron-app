import React, {useState} from "react";
import {Button, Col, Modal, Row} from 'antd'
import {TDevice} from "../../typing";
import {ChForm, ChUtils, FormItemType} from "ch-ui";
import {useForm} from "antd/es/form/Form";
import {doStartGame} from "../../call";
const { useOptionFormListHook } = ChUtils.chHooks

function usePageStore() {
    const [formRef] = useForm()
    const [linkDeviceId, setLinkDeviceId] = useState<number|undefined>()
    const [showSelectDeviceModal, setShowSelectDeviceModal] = useState<boolean>(false)
    const {optionsMap: deviceMap, options: deviceOptions} = useOptionFormListHook({url: '/api/device/get_device_list', query: {}})

    const handleClickLinkDevice = (device: TDevice) => {
        const owurl = `http://103.100.210.203:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
        const tmp:any = window.open(owurl, "",  'height=740, width=360, top=200, left=700')
        tmp.focus();
    }

    const handleSelectJiangjunDevice = () => {
        formRef.validateFields().then((res: any) => {
            if(res.deviceId) {
                const device: TDevice = deviceMap[res.deviceId]
                handleClickLinkDevice(device)
                setShowSelectDeviceModal(false)
                console.log(doStartGame({}))
            }
        })
    }

    return {
        formRef,
        linkDeviceId,
        setLinkDeviceId,
        deviceOptions,
        handleClickLinkDevice,
        handleSelectJiangjunDevice,
        showSelectDeviceModal,
        setShowSelectDeviceModal
    }
}

function Home() {
    const pageStore = usePageStore()
    return <div>
        <div>
            <div>报警处理</div>
            <div className='flex'>
                <div>机器1</div>
                <div>警告</div>
                <div>报警信息</div>
            </div>
        </div>
        <Row>
            <Col>
                <Button onClick={()=>{
                    pageStore.setShowSelectDeviceModal(true)
                }}>一件起号</Button>
            </Col>
        </Row>
        <Modal footer={false} visible={pageStore.showSelectDeviceModal}>
            <ChForm onFinish={()=>{pageStore.handleSelectJiangjunDevice()}} form={pageStore.formRef} formData={[{ type: FormItemType.select, label: '选择设备', name: 'deviceId', options: pageStore.deviceOptions}]}/>
        </Modal>
    </div>
}

export default Home
