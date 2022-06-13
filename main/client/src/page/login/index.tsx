import React from 'react'
import './index.less'
import { ChForm, ChUtils, FormItemType } from "ch-ui";
import { Button } from "antd";
import { useForm } from "antd/es/form/Form";
import { UserStore } from "../../store/userStore";


function Login() {
    const userStore = UserStore.useContainer()
    const [formRef] = useForm()
    const handleClickLoginButton = () => {
        // userStore.setUser({
        //     id: 1,
        //     username: 'kuke',
        //     password: '123456'
        // })
        // userStore.setIsLogin(true)
        formRef.validateFields().then(
        (user)=>  ChUtils.Ajax.request({
            url: '/api/user/login',
            data: user,
            method: 'post'
        }).then((res:{
            data: string,
            status: number,
        })=> {
            if(res.data) {
                userStore.setUser(user)
                userStore.setIsLogin(true)
                userStore.setToken(res.data)
                // @ts-ignore

            }
        }))
        // () => {

        // })

    }
    return <div className='login-page page flex-column-all-center'>
        <div className='login-form'>
            <ChForm
                form={formRef}
                formData={[{
                    rules: [{ required: true, message: '用户名不能为空' }],
                    type: FormItemType.input,
                    name: 'username',
                    label: '用户名',
                    key: 'username',
                    placeholder: '请输入用户名'
                }, {
                    rules: [{ required: true, message: '密码不能为空' }],
                    type: FormItemType.password,
                    name: 'password',
                    label: '密码',
                    key: 'password',
                    placeholder: '请输入密码'
                }]} />
        </div>
        <Button onClick={handleClickLoginButton} className='login-button' type='primary'>登录</Button>
    </div>
}
export default () => <Login />
