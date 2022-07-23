import React, { useEffect, useState } from 'react'
import { UserStore } from "../store/userStore"
import { HomePageStore } from "../page/home"
import './index.less'
import { ChLayout } from 'ch-ui'
import { Breadcrumb, Popover, Menu } from 'antd';
import image_robot from '../assets/images/icon.jpg';
// @ts-ignore
import { ContactsOutlined, MobileOutlined, CalendarOutlined, DashboardOutlined, TransactionOutlined } from '@ant-design/icons';
import { useHistory, useLocation } from "react-router-dom";
import { MainThread } from "../call";
import Login from "../page/login";
interface LayoutProps {
    children: JSX.Element;
}

const routerConfigMap: any = {
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
    'task_list': {
        text: '任务列表',
        url: '',
    },
    'task_config': {
        text: '任务配置',
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
    const paths = location.pathname.split("/").filter(item => {
        return item && item != ""
    })
    const pathCount = paths.length
    console.log(paths)
    return <div className='flex'>
        <div>
            <Breadcrumb>
                {
                    paths.map((item, index) => {
                        return routerConfigMap[item] && <Breadcrumb.Item key={item}>
                            {routerConfigMap[item] && routerConfigMap[item].text}{index + 1 < pathCount ? "" : ""}
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
    const userStore = UserStore.useContainer()
    const [visiblePopoverId, setVisiblePopoverId] = useState<string>()
    useEffect(() => {
        setTimeout(() => {
            MainThread.init()
        }, 0)
    }, [])

    const handleClickMenu = (e: any, url: string) => {
        e.domEvent.stopPropagation();
        setVisiblePopoverId((v) => '')
        history.push(url)
    }

    const history = useHistory()
    const sider = {
        currentItem: 1,
        siderItems: [
            {
                text: '控制面板',
                icon: <ContactsOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/')
                },
            },
            {
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
                icon: <Popover visible={visiblePopoverId == 'taskPopover'} className='layout-task-menu' placement="right" content={
                    <Menu style={{ width: 150, textAlign: 'center' }} mode="inline">
                        <Menu.Item key="9" onClick={(e) => { handleClickMenu(e, '/task/task_list') }}>任务列表</Menu.Item>
                        <Menu.Item key="10" onClick={(e) => { handleClickMenu(e, '/task/task_config') }}>任务配置</Menu.Item>
                    </Menu>
                } trigger="click">
                    <CalendarOutlined style={{ fontSize: 24 }} />
                </Popover>,
                click: () => {
                    setVisiblePopoverId('taskPopover')
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
            },
            {
                text: '退出登录',
                icon: <TransactionOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    userStore.setIsLogin(false)
                //    window.location.href = '/login'
                }
            }
        ]
    }
    console.log('Layout 刷新')
    return userStore.isLogin ? <ChLayout header={<Header />} adminIcon={<img style={{ borderRadius: '50%', width: '60px', height: 'auto' }} src={image_robot} />} sider={sider}>
        <div className='app-content'>
            {props.children}
        </div>
    </ChLayout> : <Login />
}

export default (props: LayoutProps) => {
    // @ts-ignore
    return <UserStore.Provider> <HomePageStore.Provider>
        <Layout {...props} />
        </HomePageStore.Provider>
    </UserStore.Provider>
}

