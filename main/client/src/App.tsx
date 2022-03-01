import React from "react";
import { ChUtils } from 'ch-ui'
import Layout from './layout/index'
import './index.less'
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";
import Account from "./page/account";
import Task from "./page/task";
import Log from "./page/log";
import Device from "./page/device";
import Report from "./page/report";
import Home from "./page/home";
import {ConfigProvider} from "antd";


ChUtils.Ajax.RequestConfig.config = {
    baseURL: 'http://103.100.210.203:3000',
    headers: {
        'Content-Type': 'application/json',
    }
}

import zh_CN from 'antd/lib/locale-provider/zh_CN';

// const AccountPage = loadable(() => import('./page/account'), {
//     fallback: <Account />
// })
// const DevicePage = loadable(() => import('./page/device'), {
//     fallback:
// })

export function App() {
    return (
        <ConfigProvider locale={zh_CN}>
            <Router>
                <Layout>
                    <Switch>
                        <Route path="/account">
                            <Account />
                        </Route>
                        <Route path="/device">
                            <Device />
                        </Route>
                        <Route path="/task">
                            <Task />
                        </Route>
                        <Route path="/log">
                            <Log />
                        </Route>
                        <Route path="/report">
                            <Report />
                        </Route>
                        <Route path="/">
                            <Home/>
                        </Route>
                    </Switch>
                </Layout>
            </Router>
        </ConfigProvider>
    );
}


export default <App />
