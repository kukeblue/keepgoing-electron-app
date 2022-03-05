import { ipcRenderer } from 'electron'
import resourcePaths from './resourcePaths'

window.addEventListener("DOMContentLoaded", () => {
    // @ts-ignore
    window.ipcRenderer = ipcRenderer
    console.log(ipcRenderer.sendSync(resourcePaths.MESSAGE_INIT, 'ping'))

    ipcRenderer.on(resourcePaths.MESSAGE_INIT_REPLY, (event, arg) => {
        console.log(arg)
    })
});
