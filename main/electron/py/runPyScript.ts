// const exec = require('child_process').exec;
import {exec, spawn} from "child_process";
import {logger} from "../utils/logger";

const execSync = require('child_process').execSync;
const { resolve } = require('path')
const decoder = new TextDecoder('gbk');

const runningProcess = []

export function runPyScript(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const command = `python ${resolve('./')}/main/electron/py/${name}.py${(argsStr.length > 0 ? ` ${argsStr}` : '')}`
        console.log(command)
        const process = exec(command,  (error, stdout, stderr)=>{
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            const printText = stdout.toString().split(/\r?\n/)[0]
            console.log(printText);
        })
        console.log(process.pid)
        runningProcess.push(process.pid)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}
const reg = /\n(\n)*( )*(\n)*\n/g;
export function runPyScriptSync(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const output = execSync('python ' + resolve('./') + `/main/electron/py/${name}` + '.py' + (argsStr.length > 0 ? ` ${argsStr}` : ''))
        const log = decoder.decode(output)
        logger.info(log)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}


