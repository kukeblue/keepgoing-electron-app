// const exec = require('child_process').exec;
const execSync = require('child_process').execSync;
const { resolve } = require('path')
const iconv = require('iconv-lite');
const encoding = 'cp936';
const binaryEncoding = 'binary';

export function runPyScript(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const output = execSync('python ' + resolve('./') + '/main/electron/py/test' + '.py ' + argsStr)
        const log = output.toString()
        console.log(log)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}


