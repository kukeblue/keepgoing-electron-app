const exec = require('child_process').exec;
const execSync = require('child_process').execSync;
const { resolve } = require('path')

export function runPyScript(name, args=[]) {
    let argsStr = ''
    args.forEach((item, index)=> argsStr = argsStr + (index > 0 ? ' ' : '') + item)
    const output = execSync('python ' + resolve('./') + '\\main\\electron\\py\\' + name + '.py ' + argsStr)
    console.log('runPyScript', output.toString())
    const result = Number(output.toString())
    return Number(result)
}


