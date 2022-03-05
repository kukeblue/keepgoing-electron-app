import {ipcMain } from 'electron';
import resourcePaths from './resourcePaths'

const init = ()=>{ 
    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => {
        event.reply(resourcePaths.MESSAGE_INIT_REPLY, 'pong')
    })
    
    // ipcMain.on(resourcePaths.MESSAGE_INIT_REPLY, (event, arg) => {
    //     event.returnValue = 'pong'
    // })

    ipcMain.on(resourcePaths.METHOD_START_GAME, (event, arg) => {
        console.log('???????')
        const ret = {
            status: 0
        }
        event.returnValue = 'pong'
        // event.reply(resourcePaths.METHOD_START_GAME, JSON.stringify(ret))
    })
}
    
const MessageHadle = {
    init
}

export default MessageHadle;
