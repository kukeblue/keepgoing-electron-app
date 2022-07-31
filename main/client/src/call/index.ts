import resourcePaths from "../../../electron/resourcePaths";


export const getJiangjunCode = (body: Object) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_START_GAME, JSON.stringify(body))
export const doStartGame = (body: string[]) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_LOGIN_GAME, body)
export const doTest = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST, [])
export const doTest2 = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_TEST2, [])
export const doKillProcess = (pid: string) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_KILL_PROCESS, [pid])
export const doGetWatuInfo = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_GET_WATU_INFO, [])
export const doZhuaGuiTask = (deviceId: number) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_ZHUAGUI_TASK, [deviceId])
export const doCloseAllTask = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_CLOSE_ALL_TASK, [])
export const doThrowLitter = (deviceId: number) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_THROW_LITTER, [deviceId])
export const doSellEquipment = (deviceId: number) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_SELL_EQUIPMENT, [deviceId])
export const doConnector = () => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_CONNECTOR, [])
export const doZhandou = (deviceId: number) => {
    (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_ZHANDOU, [deviceId])
}
export const doHanghua = (num: number) => {
    (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_HANHUA, [num])
}



export const doSyncImages = (files: string[]) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_SYNC_IMAGES, files)
export const doGetWatuClickMap = (mapName: string, x: number, y: number, index: number, otherPoint?: string, isBeen?: boolean, cangkuPath?: string) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_CLICK_WATU_MAP, [mapName, x, y, index, otherPoint, isBeen, cangkuPath])
export const doBee = (cangkuPath: string) => (window as any).ipcRenderer.sendSync(resourcePaths.METHOD_BEE_MODE, [cangkuPath])


const init = () => {
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_LOG, (event: any, arg: any) => {
        messageListener.pushLogHandles.forEach(callback => {
            callback(arg)
        })
    });
    (window as any).ipcRenderer.on(resourcePaths.MESSAGE_PUSH_MAIN_STATE, (event: any, arg: any) => {
        messageListener.pushStateHandles.forEach(callback => {
            callback(arg)
        })
    });

    (window as any).ipcRenderer.on(resourcePaths.METHOD_GET_WATU_INFO_REPLY, (event: any, arg: any) => {
        console.log('methodGetWatuInfoReplyHandles ?????')
        messageListener.methodGetWatuInfoReplyHandles[0](arg)
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



