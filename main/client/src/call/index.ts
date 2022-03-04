import resourcePaths from "../../../electron/resourcePaths";

// @ts-ignore
export const doStartGame = (body: Object) => window.ipcRenderer.sendSync(resourcePaths.METHOD_START_GAME, JSON.stringify(body))