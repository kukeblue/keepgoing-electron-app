const exec = require('child_process').exec;
const execSync = require('child_process').execSync;

export function runPyScript() {
    const output = execSync('python web.py')
    console.log('sync: ' + output.toString())
}


