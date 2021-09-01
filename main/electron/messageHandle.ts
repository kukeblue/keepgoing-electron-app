import {ipcMain } from 'electron';
import resourcePaths from './resourcePaths'

const init = ()=>{ 
    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => {
        event.reply(resourcePaths.MESSAGE_INIT_REPLY, 'pong')
    })
    
    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => {
        event.returnValue = 'pong'
    })
}
    
const MessageHadle = {
    init
}

export default MessageHadle;
