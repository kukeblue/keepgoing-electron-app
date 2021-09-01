import React from "react";
import Layout from './layout/index'
import './index.less'
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";
import loadable from "@loadable/component";
import Home from "./page/home";

const HomePage = loadable(() => import('./page/home'), {
    fallback: <Home></Home>
})

export function App() {
    return (
        <Router>
            <Layout>
                <Switch>
                    <Route path="/">
                        <HomePage />
                    </Route>
                </Switch>
            </Layout>
        </Router>
    );
}


export default <App />