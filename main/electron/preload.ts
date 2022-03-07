import { ipcRenderer } from 'electron'
import resourcePaths from './resourcePaths'

window.addEventListener("DOMContentLoaded", () => {
    // @ts-ignore
    window.ipcRenderer = ipcRenderer
});
