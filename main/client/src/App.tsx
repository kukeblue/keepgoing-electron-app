import React from "react";
import { ChUtils } from 'ch-ui'
import Layout from './layout/index'
import './index.less'
import {
    HashRouter as Router,
    Switch,
    Route,
} from "react-router-dom";
import Account from "./page/account";
import Task from "./page/task";
import Log from "./page/log";
import Device from "./page/device";
import Report from "./page/report";
import Home from "./page/home";
import TaskConfig from "./page/taskConfig";
import { ConfigProvider } from "antd";

// @ts-ignore
const env = APP_ENV
// @ts-ignore
console.log('Running App version ' + APP_ENV);
ChUtils.Ajax.RequestConfig.config = {
    // @ts-ignore
    baseURL: env === 'dev' ? 'http://103.100.210.203:3000' : 'http://103.100.210.203:3000',
    headers: {
        'Content-Type': 'application/json',
        token: localStorage.getItem('token')
    }
}

import zh_CN from 'antd/lib/locale-provider/zh_CN';
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
                        <Route path="/task/task_list">
                            <Task />
                        </Route>
                        <Route path="/task/task_config">
                            <TaskConfig />
                        </Route>
                        <Route path="/log">
                            <Log />
                        </Route>
                        <Route path="/report">
                            <Report />
                        </Route>
                        <Route path="/">
                            <Home />
                        </Route>
                    </Switch>
                </Layout>
            </Router>
        </ConfigProvider>
    );
}


export default <App />
