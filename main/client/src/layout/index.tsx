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
import moment from 'moment'
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
    const userStore = UserStore.useContainer()
    const username = userStore.user?.username
    return <div className='flex p-header'>
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
        <div className='user-avatar'>
            <div>当前账号: {username}</div>
            <div>vip到期时间: {userStore.user?.vipCard && moment(userStore.user?.vipCard?.endTime * 1000).format('YYYY-MM-DD')}</div>
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
    const level = userStore.user?.vipCard.level
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
                icon: <CalendarOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/account')
                },
            },
            {
                text: '收益管理',
                icon: <TransactionOutlined style={{ fontSize: 24 }} />,
                click: () => {
                    history.push('/report')
                },
            }
           
        ]
    }
    if(level && level > 999) {
        sider.siderItems.push({
            text: '用户管理',
            icon: <TransactionOutlined style={{ fontSize: 24 }} />,
            click: () => {
                history.push('/user')
            },
        })
    }
    sider.siderItems.push({
        text: '退出登录',
        icon: <TransactionOutlined style={{ fontSize: 24 }} />,
        click: () => {
            userStore.setIsLogin(false)
            //    window.location.href = '/login'
        }
    })
    
    // @ts-ignore
    return userStore.isLogin ? 
        <div className='app-content'>
            {props.children}
        </div>
    : <Login />
}

export default (props: LayoutProps) => {
    // @ts-ignore
    return <UserStore.Provider> <HomePageStore.Provider>
        <Layout {...props} />
    </HomePageStore.Provider>
    </UserStore.Provider>
}

