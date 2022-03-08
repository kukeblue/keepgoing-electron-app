import {ipcMain } from 'electron';
import resourcePaths from './resourcePaths'
import {runPyScript} from "./py/runPyScript";

const init = ()=>{
    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => {
        // event.reply(resourcePaths.MESSAGE_INIT_REPLY, 'pong')
    })
    ipcMain.on(resourcePaths.METHOD_START_GAME, (event, arg) => {
        console.log('runPyScript getGameVerificationCode')
        const result = runPyScript('getGameVerificationCode')
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    ipcMain.on(resourcePaths.METHOD_LOGIN_GAME, (event, args: string[]) => {
        console.log('runPyScript getGameVerificationCode')
        const result = runPyScript('loginGame', args)
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    ipcMain.on(resourcePaths.METHOD_TEST, (event, args) => {
        console.log('message handle: test')
        const result = runPyScript('test', args)
        event.returnValue = {
            code: result,
            status: 0
        }
    })
}

const MessageHadle = {
    init
}

export default MessageHadle;
