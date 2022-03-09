import resourcePaths from "../../../electron/resourcePaths";


export const getJiangjunCode = (body: Object) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_START_GAME, JSON.stringify(body))
export const doStartGame = (body: string[]) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_LOGIN_GAME, body)
export const doTest = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST, [])
export const doTest2 = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST2, [])
export const doKillProcess = (pid: string) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_KILL_PROCESS, [pid])



const init = () => {
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_LOG, (event: any, arg: any) => {
        messageListener.pushLogHandles.forEach(callback=>{
            callback(arg)
        })
    });
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_MAIN_STATE, (event: any, arg: any) => {
        messageListener.pushStateHandles.forEach(callback=>{
            console.log(arg)
            callback(arg)
        })
    });
}

export const messageListener: {
    pushLogHandles: Function[]
    pushStateHandles: Function[]
} = {
    pushLogHandles: [],
    pushStateHandles: []
}


export const MainThread = {
    hasInit: false,
    messageListener,
    init,
}



