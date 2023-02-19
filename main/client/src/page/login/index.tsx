import React from 'react'
import './index.less'
import { ChForm, ChUtils, FormItemType } from "ch-ui";
import { Button } from "antd";
import { useForm } from "antd/es/form/Form";
import { UserStore } from "../../store/userStore";
import { setOption } from "../../call";


function Login() {
    const userStore = UserStore.useContainer()
    const [formRef] = useForm()
    const handleClickLoginButton = () => {

        // userStore.setIsLogin(true)
        formRef.validateFields().then(
            (user) => ChUtils.Ajax.request({
                url: '/api/user/login2',
                data: {
                    username:user.username,
                    password: '123456'
                },
                method: 'post'
            }).then((res: {
                data: {
                    token: string,
                    user: any,
                },
                status: number,
            }) => {
                if (res.data) {
                    userStore.setUser(res.data.user)
                    userStore.setIsLogin(true)
                    userStore.setToken(res.data.token)
                    setTimeout(()=>{
                        const id = res.data.user.id
                        if(id) {
                            setOption(id)
                            location.reload()
                        }
                    }, 2000)
                    // @ts-ignore
                }
            }))

    }
    return <div className='login-page page flex-column-all-center'>
        <div className='login-form'>
            <ChForm
                form={formRef}
                formData={[{
                    // rules: [{ required: true, message: '用户名不能为空' }],
                    type: FormItemType.input,
                    name: 'username',
                    label: '请输入卡号',
                    key: 'username',
                    placeholder: '请输入卡号'
                }]} />
        </div>
        <Button onClick={handleClickLoginButton} className='login-button'>登录</Button>
    </div>
}
export default () => <Login />
