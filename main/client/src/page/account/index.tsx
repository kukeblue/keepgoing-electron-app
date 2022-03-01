import { Button } from 'antd';
import React from "react";
import './index.less'
import {ChTablePanel} from "ch-ui";

function Account() {
    return <div className='home'>
        <ChTablePanel
            disablePagination
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
                    title: '运行手机',
                    dataIndex: 'phone',
                    key: 'phone',
                },
                {
                    title: '是否在线',
                    dataIndex: 'online',
                    key: 'online',
                },
                {
                    title: '操作',
                    dataIndex: 'option',
                    key: 'option',
                }
            ]}  url='/api/game_account/get_game_account_page'
            formData={[]}/>
    </div>
}

export default Account;
