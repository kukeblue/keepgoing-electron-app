import resourcePaths from "../../../electron/resourcePaths";

// @ts-ignore
export const getJiangjunCode = (body: Object) => window.ipcRenderer.sendSync(resourcePaths.METHOD_START_GAME, JSON.stringify(body))
// @ts-ignore
export const doStartGame = (body: string[]) => window.ipcRenderer.sendSync(resourcePaths.METHOD_LOGIN_GAME, body)
