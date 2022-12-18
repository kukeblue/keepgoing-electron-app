import { ipcMain } from 'electron';
import resourcePaths from './resourcePaths'
import { runPyScript, runPyScriptSync } from "./py/runPyScript";
import { logger } from "./utils/logger";
import state, { AppChildProcess } from "./state";
import { syncServeImages } from './utils/resourceFileManage'

export let messageSender: {
    sendLog: Function
    sendState: Function
    sendGetWutuInfo: Function
} = null

function buildSender(mainWindow: Electron.BrowserWindow) {
    return {
        sendLog(log) {
            mainWindow.webContents.send(resourcePaths.MESSAGE_PUSH_LOG, log);
        },
        sendState() {
            mainWindow.webContents.send(resourcePaths.MESSAGE_PUSH_MAIN_STATE, state);
        },
        // 发送挖图结果
        sendGetWutuInfo(body: { result: any[] }) {
            mainWindow.webContents.send(resourcePaths.METHOD_GET_WATU_INFO_REPLY, body);
        }
    }
}

const init = (mainWindow: Electron.BrowserWindow) => {
    // 注册信鸽
    MessageHandle.messageSender = buildSender(mainWindow)

    ipcMain.on(resourcePaths.MESSAGE_INIT, (event, arg) => { })
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
        const result = runPyScript('ddServer', args)
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
     // 注入配置
     ipcMain.on(resourcePaths.METHOD_SET_OPTION, (event, args) => {
        logger.info('run py script: mhSetOption')
        const result = runPyScript('mhSetOption', ["start" ,...args] )
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 读取宝图
    ipcMain.on(resourcePaths.METHOD_GET_WATU_INFO, (event, args) => {
        logger.info('run py script: METHOD_GET_WATU_INFO')
        const result = runPyScript('mhWatu', ['info', [...args]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 抓鬼
    ipcMain.on(resourcePaths.METHOD_ZHUAGUI_TASK, (event, args) => {
        logger.info('run py script: METHOD_ZHUAGUI_TASK')
        const result = runPyScript('mhZhuaGui', ['zg', [...args]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 补店
    ipcMain.on(resourcePaths.METHOD_BUDIAN_TASK, (event, args) => {
        logger.info('run py script: METHOD_BUDIAN_TASK')
        const result = runPyScript('mhBudian', ['lf', [...args]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 关闭所有进程
    ipcMain.on(resourcePaths.METHOD_CLOSE_ALL_TASK, (event, args) => {
        logger.info('run py script: METHOD_CLOSE_ALL_TASK')
        const result = runPyScript('closeAllMhTask', [])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 丢垃圾
    ipcMain.on(resourcePaths.METHOD_THROW_LITTER, (event, args) => {
        logger.info('run py script: METHOD_THROW_LITTER')
        const result = runPyScript('mhThrowLitter', ['start', args[0]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 卖装备
    ipcMain.on(resourcePaths.METHOD_SELL_EQUIPMENT, (event, args) => {
        logger.info('run py script: METHOD_SELL_EQUIPMENT')
        const result = runPyScript('mhSellEquipment', ['start', args[0]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 连点器
    ipcMain.on(resourcePaths.METHOD_CONNECTOR, (event, args) => {
        logger.info('run py script: METHOD_CONNECTOR')
        const result = runPyScript('mhLianDian', ['start', []])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 带队战斗
    ipcMain.on(resourcePaths.METHOD_HANHUA, (event, args) => {
        logger.info('run py script: METHOD_HANHUA')
        const result = runPyScript('mhZhandou', ['hh', args[0]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 更新PY
    ipcMain.on(resourcePaths.METHOD_UPDATEPY, (event, args) => {
        logger.info('run py script: METHOD_UPDATEPY')
        const result = runPyScript('mhUpdate', [])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 带队打架
    ipcMain.on(resourcePaths.METHOD_ZHANDOU, (event, args) => {
        logger.info('run py script: METHOD_ZHANDOU')
        const result = runPyScript('mhZhandou', ['lbc', args[0]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 小蜜蜂模式
    ipcMain.on(resourcePaths.METHOD_BEE_MODE, (event, args) => {
        logger.info('run py script: METHOD_BEE_MODE')
        const result = runPyScript('mhWatu', ['bee', args[0], args[1], 'None', args[2]])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 点击小地图
    ipcMain.on(resourcePaths.METHOD_CLICK_WATU_MAP, (event, args) => {
        logger.info('run py script: METHOD_CLICK_WATU_MAP')
        const result = runPyScript('mhWatu', ['clickMap', ...args])
        event.returnValue = {
            code: result,
            status: 0
        }
    })
    // 同步图片到本地
    ipcMain.on(resourcePaths.METHOD_SYNC_IMAGES, (event, args) => {
        logger.info('run py script: METHOD_SYNC_IMAGES', args)
        syncServeImages(args)
        event.returnValue = {
            data: {
                success: true
            },
            status: 0
        }
    })
    // 杀死进程
    ipcMain.on(resourcePaths.METHOD_KILL_PROCESS, (event, args) => {
        logger.info('run py script: ' + 'METHOD_KILL_PROCESS')
        const pid = Number(args[0])
        const runningPyProcess = state.runningPyProcess
        Object.keys(runningPyProcess).find((key) => {
            if (runningPyProcess[key] == pid) {
                delete runningPyProcess[key]
                if (AppChildProcess[key]) {
                    logger.info('run py script: find python pid key:' + AppChildProcess[key])
                    runPyScriptSync('killProcess', [AppChildProcess[key]])
                    delete AppChildProcess[key]
                }
                logger.info('run py script: find pid key:' + key)
                return true
            }
        })
        runPyScriptSync('killProcess', args)
        event.returnValue = {
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
