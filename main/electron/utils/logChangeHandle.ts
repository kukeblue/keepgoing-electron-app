import MessageHandle from "../messageHandle";
import {AppChildProcess} from "../state";
import {logger} from "./logger";

const fs = require('fs');

export const listenLogs = function(filePath){
    console.log(`log ${filePath} listen...`);
    let fileOPFlag="a+";
    fs.open(filePath,fileOPFlag,function(error,fd){
        let buffer;
        let remainder = null;
        fs.watchFile(filePath,{
            persistent: true,
            interval: 1000
        },function(curr, prev){
            if(curr.mtime>prev.mtime){
                buffer =  Buffer.alloc(curr.size - prev.size);
                fs.read(fd,buffer,0,(curr.size - prev.size),prev.size,function(err, bytesRead, buffer){
                    generateTxt(buffer.toString())
                });
            }else{
            }
        });
        function generateTxt(str){
            let temp = str.split('\r\n');
            for(let s in temp){
                if(MessageHandle.messageSender) {
                    const str = temp[s]
                    if(str.includes('pythonPid')) {
                        const data = str.split('|')
                        const length = data.length
                        const pid = data[length - 1]
                        const fileName = data[length - 2]
                        AppChildProcess[fileName] = pid
                        logger.info('add py id ' + fileName + pid)
                    }
                    MessageHandle.messageSender.sendLog(str)
                }
            }
        }
    });
}

