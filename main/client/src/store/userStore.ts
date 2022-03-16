import { useEffect, useState } from "react";
import { createContainer } from "unstated-next"
import { TUser } from "../typing";
import {ChUtils} from "ch-ui";
function useUserStore() {
    const [user, setUser] = useState<TUser>()
    const [isLogin, setIsLogin] = useState<boolean>(!!localStorage.getItem('token'))
    const [token, setToken] = useState<string>(localStorage.getItem('token') || '')
    useEffect(()=>{
        if(token) {
            // @ts-ignore
            if(ChUtils.Ajax.RequestConfig.config.headers) {
                // @ts-ignore
                ChUtils.Ajax.RequestConfig.config.headers.token = token
            }
        }
    },[])
    useEffect(() => {
        if(token) {
            localStorage.setItem('token', token)
            // @ts-ignore
            if(ChUtils.Ajax.RequestConfig.config.headers) {
                // @ts-ignore
                ChUtils.Ajax.RequestConfig.config.headers.token = token
            }
        }
    }, [token])
    useEffect(() => {
        if(user) {
            ChUtils.chCache.setObCache('user', user)
        }
    }, [user])
    return {
        token,
        setToken,
        isLogin,
        setIsLogin,
        user,
        setUser
    }
}

export const UserStore = createContainer(useUserStore)
