import React from 'react'
import { UserStore } from "../store/userStore"
import './index.less'
import { ChLayout } from 'ch-ui'
import { Breadcrumb } from 'antd';
import image_robot from '../assets/images/robot.png';


import {
    ContactsOutlined,
    MobileOutlined,
    CalendarOutlined,
    DashboardOutlined,
    TransactionOutlined
} from '@ant-design/icons';
import {useHistory, useLocation} from "react-router-dom";
interface LayoutProps {
    children: JSX.Element;
}

const routerConfigMap:any = {
    'device': {
        text: '设备',
        url: '',
    },
    'account': {
        text: '账号',
        url: '',
    },
    'task': {
        text: '任务',
        url: '',
    },
    'log': {
        text: '任务日志',
        url: '',
    },
    'report': {
        text: '报表',
        url: '',
    }
}

function Header() {
    const location = useLocation();
    const paths = location.pathname.split("/").filter(item=>{
        return item && item != ""
    })
    const pathCount = paths.length
    console.log(paths)
    return <div className='flex'>
        <div>
            <Breadcrumb>
                {
                    paths.map((item, index)=>{
                        return  <Breadcrumb.Item>
                            {routerConfigMap[item].text}{index + 1 < pathCount ? "/" : ""}
                        </Breadcrumb.Item>
                    })
                }
                {/*<Breadcrumb.Item>*/}
                {/*    <a href="">Application Center</a>*/}
                {/*</Breadcrumb.Item>*/}
                {/*<Breadcrumb.Item>*/}
                {/*    <a href="">Application List</a>*/}
                {/*</Breadcrumb.Item>*/}
                {/*<Breadcrumb.Item>An Application</Breadcrumb.Item>*/}
            </Breadcrumb>
        </div>
    </div>
}

function Layout(props: LayoutProps) {
    const history = useHistory()
    const sider = {
        currentItem: 1,
        siderItems: [{
                text: '账号管理',
                icon: <ContactsOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/account')
                },
            },
            {
                text: '设备管理',
                icon: <MobileOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/device')
                }
            },
            {
                text: '任务管理',
                icon: <CalendarOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/task')
                }
            },
            {
                text: '任务日志',
                icon: <DashboardOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/log')
                }
            },
            {
                text: '收支报表',
                icon: <TransactionOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/report')
                }
            }
        ]
    }
    return <ChLayout header={<Header/>} adminIcon={<img style={{width: '60px', height: 'auto'}} src={image_robot}/>} sider={sider}>
        <div className='app-content'>
            {props.children}
        </div>
    </ChLayout>
}

export default (props: LayoutProps) => <UserStore.Provider><Layout {...props}></Layout></UserStore.Provider>;
