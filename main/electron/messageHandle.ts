import {ipcMain } from 'electron';
import resourcePaths from './resourcePaths'
import {runPyScript, runPyScriptSync} from "./py/runPyScript";
import {logger} from "./utils/logger";
const fs = require('fs')

export let messageSender:{
    sendLog: Function
} = null

function buildSender(mainWindow: Electron.BrowserWindow) {
    return {
        sendLog(log) {
            mainWindow.webContents.send(resourcePaths.MESSAGE_PUSH_LOG, log);
        }
    }
}

const init = (mainWindow: Electron.BrowserWindow)=>{
    // 注册信鸽
    MessageHandle.messageSender = buildSender(mainWindow)

    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => {})
    // 获取将军令
    ipcMain.on(resourcePaths.METHOD_START_GAME, (event, arg) => {
        logger.info('run py script: get game verificationCode')
        const result = runPyScriptSync('getGameVerificationCode')
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 一键起号
    ipcMain.on(resourcePaths.METHOD_LOGIN_GAME, (event, args: string[]) => {
        logger.info('run py script: loginGame')
        const result = runPyScript('loginGame', args)
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 测试
    ipcMain.on(resourcePaths.METHOD_TEST, (event, args) => {
        logger.info('run py script: test')
        const result = runPyScriptSync('test', args)
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 异步测试
    ipcMain.on(resourcePaths.METHOD_TEST2, (event, args) => {
        logger.info('run py script: test')
        const result = runPyScript('asyncTest', args)
        event.returnValue = {
            code: result,
            status: 0
        }
    })
}

const MessageHandle = {
    init,
    buildSender,
    messageSender,
}

export default MessageHandle;
