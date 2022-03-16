import resourcePaths from "../../../electron/resourcePaths";


export const getJiangjunCode = (body: Object) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_START_GAME, JSON.stringify(body))
export const doStartGame = (body: string[]) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_LOGIN_GAME, body)
export const doTest = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST, [])
export const doTest2 = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST2, [])
export const doKillProcess = (pid: string) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_KILL_PROCESS, [pid])
export const doGetWatuInfo = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_GET_WATU_INFO, [])



const init = () => {
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_LOG, (event: any, arg: any) => {
        messageListener.pushLogHandles.forEach(callback=>{
            callback(arg)
        })
    });
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_MAIN_STATE, (event: any, arg: any) => {
        messageListener.pushStateHandles.forEach(callback=>{
            callback(arg)
        })
    });

    (window as any).ipcRenderer.on(resourcePaths.METHOD_GET_WATU_INFO_REPLY, (event: any, arg: any) => {
        messageListener.methodGetWatuInfoReplyHandles.forEach(callback=>{
            callback(arg)
        })
    });
}

export const messageListener: {
    pushLogHandles: Function[]
    pushStateHandles: Function[]
    methodGetWatuInfoReplyHandles: Function[]
} = {
    pushLogHandles: [],
    pushStateHandles: [],
    methodGetWatuInfoReplyHandles: []
}


export const MainThread = {
    hasInit: false,
    messageListener,
    init,
}



