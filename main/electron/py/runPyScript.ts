// const exec = require('child_process').exec;
import {exec, spawn} from "child_process";
import {logger} from "../utils/logger";
import state from "../state";

const execSync = require('child_process').execSync;
const { resolve } = require('path')
const decoder = new TextDecoder('gbk');




export function runPyScript(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const command = `python ${resolve('./')}/main/electron/py/${name}.py${(argsStr.length > 0 ? ` ${argsStr}` : '')}`
        logger.info('run py script ' + command)
        const process = exec(command,  (error, stdout, stderr)=>{
            delete state.runningPyProcess[name]
            if (error) {
                logger.info(`exec error: ${error}`);
                return;
            }else {
                logger.info(`${name} run finish pid ${state.runningPyProcess[name]}`)
            }
        })
        state.runningPyProcess[name] = process.pid
        logger.info('pid: ' + process.pid)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}

export function runPyScriptSync(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const output = execSync('python ' + resolve('./') + `/main/electron/py/${name}` + '.py' + (argsStr.length > 0 ? ` ${argsStr}` : ''))
        const log = decoder.decode(output)
        logger.info(log)
        logger.info(`${name} run finish`)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}


