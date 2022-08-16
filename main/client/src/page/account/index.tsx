import { Button } from 'antd';
import React from "react";
import './index.less'
import { ChTablePanel, FormItemType } from "ch-ui";

function Account() {
    return <div className='home page'>
        <ChTablePanel
            searchFormData={[
                {
                    label: '服务器',
                    name: 'gameServer',
                    type: FormItemType.input,
                    layout: {
                        span: 4
                    }
                }, {
                    label: '名字',
                    name: 'name',
                    type: FormItemType.input,
                    layout: {
                        offset: 1,
                        span: 4
                    }
                }, {
                    label: '游戏id',
                    name: 'nickName',
                    type: FormItemType.input,
                    layout: {
                        offset: 1,
                        span: 4
                    }
                }
            ]}
            urlAdd='/api/game_account/add_game_account'
            urlDelete='/api/game_account/delete_game_account'
            urlUpdate='/api/game_account/add_game_account'
            columns={[
                {
                    title: '名称',
                    dataIndex: 'name',
                    key: 'name',
                },
                {
                    title: '昵称',
                    dataIndex: 'nickName',
                    key: 'nickName',
                },
                {
                    title: '账号',
                    dataIndex: 'username',
                    key: 'username',
                },
                {
                    title: '游戏服务器',
                    dataIndex: 'gameServer',
                    key: 'gameServer',
                },
                // {
                //     title: '运行手机',
                //     dataIndex: 'phone',
                //     key: 'phone',
                // },
                // {
                //     title: '是否在线',
                //     dataIndex: 'online',
                //     key: 'online',
                // },
                // {
                //     title: '操作',
                //     dataIndex: 'option',
                //     key: 'option',
                // }
            ]}
            url='/api/game_account/get_game_account_page'
            formData={[
                {
                    type: FormItemType.input,
                    label: '账号名称',
                    name: 'name',
                    key: 'name',
                },
                {
                    type: FormItemType.input,
                    label: '游戏id',
                    name: 'nickName',
                    key: 'nickName',
                },
                {
                    type: FormItemType.input,
                    label: '账号',
                    name: 'username',
                    key: 'username',
                },
                {
                    type: FormItemType.input,
                    inputtype: 'number',
                    label: '等级',
                    name: 'level',
                    key: 'level',
                },
                {
                    type: FormItemType.input,
                    label: '密码（全部写0）',
                    name: 'password',
                    key: 'ip',
                },
                {
                    type: FormItemType.input,
                    label: 'gameServer',
                    name: 'gameServer',
                    key: 'gameServer',
                },
                {
                    type: FormItemType.select,
                    label: '状态',
                    name: 'online',
                    key: 'online',
                    options: [{
                        label: '在线',
                        value: '在线',
                    }, {
                        label: '离线',
                        value: '离线',
                    }]
                }
            ]} />
    </div>
}

export default Account;
