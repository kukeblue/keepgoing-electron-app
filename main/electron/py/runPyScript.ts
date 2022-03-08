// const exec = require('child_process').exec;
const execSync = require('child_process').execSync;
const { resolve } = require('path')
const iconv = require('iconv-lite');
const encoding = 'cp936';
const binaryEncoding = 'binary';
const decoder = new TextDecoder('gbk');
export function runPyScript(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    try {
        const output = execSync('python ' + resolve('./') + `/main/electron/py/${name}` + '.py' + (argsStr.length > 0 ? ` ${argsStr}` : ''))
        const log = decoder.decode(output)
        console.log(log)
        return 0
    }catch (error) {
        console.log(error.message)
        return 0
    }
}


