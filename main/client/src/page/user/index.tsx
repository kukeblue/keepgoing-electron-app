import { Button, Dropdown, Menu, message, Modal, Badge, Collapse  } from 'antd';
import React, { useRef, useState } from "react";
import './index.less'
import { ChForm, ChTablePanel, FormItemType, ChUtils } from "ch-ui";
import { useForm } from "antd/es/form/Form";
import { TDevice } from "../../typing";
import html2canvas from 'html2canvas';
import moment from 'moment'
const { useOptionFormListHook } = ChUtils.chHooks
const request = ChUtils.Ajax.request
const { Panel } = Collapse;
function Device() {
    const pageStore = useDevicePageStore()
    return <div className='user-page page'>
        <div className='flex'>
            <div className='device-list'>
                <ChTablePanel
                    columns={[
                        {
                            title: '账号',
                            dataIndex: 'username',
                            key: 'username',
                        },
                        {
                            title: 'VIP卡号',
                            dataIndex: 'vipCardId',
                            key: 'vipCardId',
                        }
                    ]}
                    urlUpdate='/api/user/create_user'
                    urlAdd='/api/user/create_user'
                    url='/api/user/get_user_page'
                    searchFormData={[
                        {
                            type: FormItemType.input,
                            label: '账号',
                            name: 'username',
                            key: 'username',
                            layout: {
                                span: 4
                            }
                        },
                    ]}
                    formData={[
                        {
                            type: FormItemType.input,
                            label: '账号',
                            name: 'username',
                            key: 'username',
                        },
                        {
                            type: FormItemType.input,
                            label: '密码',
                            name: 'password',
                            key: 'password',
                        },
                        {
                            type: FormItemType.input,
                            label: 'vip卡号',
                            name: 'vipCardId',
                            key: 'vipCardId',
                        },
                    ]} />
            </div>
        </div>
        <br/>
        <Collapse>
        <Panel header="会员卡管理" key="1">
        <ChTablePanel
                    onEditFormat={(item)=>{
                        item.createdTime = moment(item.createdTime * 1000).format('YYYY-MM-DD')
                        item.endTime = moment(item.endTime * 1000).format('YYYY-MM-DD')
                    }}
                    columns={[
                        {
                            title: '卡号',
                            dataIndex: 'id',
                            key: 'id',
                        },
                        {
                            title: 'level',
                            dataIndex: 'level',
                            key: 'level',
                        },
                        {
                            title: '开始时间',
                            dataIndex: 'createdTime',
                            key: 'createdTime',
                            render: (createdTime: string)=> {
                                return <div>
                                    {moment(Number(createdTime) * 1000).format('YYYY-MM-DD')}
                                </div>
                            }
                        },
                        {
                            title: '结束时间',
                            dataIndex: 'endTime',
                            key: 'endTime',
                            render: (endTime: string)=> {
                                return <div>
                                    {moment(Number(endTime) * 1000).format('YYYY-MM-DD')}
                                </div>
                            }
                        }
                    ]}
                    urlUpdate='/api/user/save_vip_card'
                    urlAdd='/api/user/save_vip_card'
                    url='/api/user/get_vip_card_page'
                    searchFormData={[
                        {
                            type: FormItemType.input,
                            label: 'id',
                            name: 'id',
                            key: 'id',
                            layout: {
                                span: 4
                            }
                        },
                    ]}
                    formData={[
                        {
                            type: FormItemType.date,
                            label: '开始时间',
                            name: 'createdTime',
                            key: 'createdTime',
                        },
                        {
                            type: FormItemType.date,
                            label: '结束时间',
                            name: 'endTime',
                            key: 'endTime',
                        },
                        {
                            type: FormItemType.input,
                            label: '会员等级',
                            name: 'level',
                            key: 'level',
                        },
                    ]} />
        </Panel>
      </Collapse>
    </div>
}

function useDevicePageStore() {
    // const [isAddTaskModalVisible, setIsAddTaskModalVisible] = useState(false);
    // const [currentPhoneUrl, setCurrentPhoneUrl] = useState('');
    // const { options: accountOptions } = useOptionFormListHook({ url: '/api/game_account/get_game_account_options', query: {}, expiresTime: 5 })
    // const { options: deviceOptions } = useOptionFormListHook({ url: '/api/device/get_device_list', query: {}, expiresTime: 5 })
    // const tableRef = useRef<{
    //     reload: Function
    // }>()
    // const [formRef] = useForm()
    // const handleClickLinkDevice = (device: TDevice) => {
    //     const owurl = `http://192.168.0.11:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
    //     const tmp: any = window.open(owurl, "", 'height=1920, width=1080, top=0, left=0')
    //     tmp.focus();
    // }
    // const handleClickPreviewDevice = (device: TDevice) => {
    //     const owurl = `http://192.168.0.11:8888/vnc.html?host=${device.ip}&port=5900&autoconnect=true&resize=scale&quality=1&compression=1`;
    //     setCurrentPhoneUrl(owurl)
    // }
    // const handleClickReadToken = () => {
    //     // @ts-ignore
    //     const a = window.document.querySelector('#appBody').querySelector('body')
    //     console.log(a)
    //     // @ts-ignore
    //     html2canvas(window.document.querySelector(body), { useCORS: true }).then(function (canvas) {
    //         // @ts-ignore
    //         window.document.querySelector('.device-list').appendChild(canvas);
    //     });
    // }
    // function handleCreateTask() {
    //     setIsAddTaskModalVisible(true)
    // }
    // function handleCloseCreateTaskModal() {
    //     setIsAddTaskModalVisible(false)
    // }
    // function handleSaveTask() {
    //     formRef.validateFields().then((res: any) => {
    //         request({
    //             url: '/api/task/create_task',
    //             data: {
    //                 name: "主线打图",
    //                 deviceId: res.deviceId,
    //                 accountId: res.accountId,
    //             },
    //             method: "post"
    //         }).then(res => {
    //             if (res.status === 0) {
    //                 handleCloseCreateTaskModal()
    //                 message.success('任务创建成功')
    //                 tableRef.current!.reload()
    //             }
    //         })
    //     })
    // }

    return {
        // currentPhoneUrl,
        // setCurrentPhoneUrl,
        // formRef,
        // deviceOptions,
        // accountOptions,
        // handleSaveTask,
        // handleCloseCreateTaskModal,
        // handleCreateTask,
        // handleClickPreviewDevice,
        // isAddTaskModalVisible,
        // setIsAddTaskModalVisible,
        // tableRef,
        // handleClickLinkDevice,
        // handleClickReadToken
    }
}

export default Device;
