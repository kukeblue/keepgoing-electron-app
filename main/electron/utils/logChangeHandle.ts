import MessageHandle from "../messageHandle";
import { AppChildProcess } from "../state";
import { logger } from "./logger";
const fs = require('fs');

export const listenLogs = function (filePath) {
    console.log(`log ${filePath} listen...`);
    let fileOPFlag = "a+";
    fs.open(filePath, fileOPFlag, function (error, fd) {
        let buffer;
        let remainder = null;
        fs.watchFile(filePath, {
            persistent: true,
            interval: 1000
        }, function (curr, prev) {
            if (curr.mtime > prev.mtime) {
                buffer = Buffer.alloc(curr.size - prev.size);
                fs.read(fd, buffer, 0, (curr.size - prev.size), prev.size, function (err, bytesRead, buffer) {
                    generateTxt(buffer.toString())
                });
            } else {
            }
        });
        function generateTxt(str) {
            let temp = str.split('\r\n');
            let mhWatuCount = 0
            for (let s in temp) {
                if (MessageHandle.messageSender) {
                    const str = temp[s]
                    if (str.includes('pythonPid')) {
                        const data = str.split('|')
                        const length = data.length
                        const pid = data[length - 1]
                        const fileName = data[length - 2]
                        AppChildProcess[fileName] = pid
                        logger.info('add py id ' + fileName + pid)
                    }
                    if (str.includes('mhWatu result')) {
                        if (mhWatuCount == 0) {
                            handleWutuFinish(str)
                            mhWatuCount = mhWatuCount + 1
                        }
                        // fs.writeFileSync(filePath, '------')
                    }
                    MessageHandle.messageSender.sendLog(str)
                }
            }
        }
    });
}

function handleWutuFinish(log: string) {
    let result = log.match(/start(.*)end/)[1]
    console.log('handleWutuFinish', result);
    MessageHandle.messageSender.sendGetWutuInfo({
        result: JSON.parse(result)
    })
}


