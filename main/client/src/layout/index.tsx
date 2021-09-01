import React from 'react'
import { UserStore } from "../store/userStore"
import './index.less'
import { ChLayout } from 'ch-ui'
import {
    VideoCameraOutlined,
} from '@ant-design/icons';
interface LayoutProps {
    children: JSX.Element;
}
function Layout(props: LayoutProps) {
    const sider = {
        siderItems: [{
            text: '脚本管理',
            icon: <VideoCameraOutlined style={{ fontSize: 24 }} />,
            click: () => { }
        }]
    }
    return <ChLayout sider={sider}>
        {props.children}
    </ChLayout>
}

export default (props: LayoutProps) => <UserStore.Provider><Layout {...props}></Layout></UserStore.Provider>;