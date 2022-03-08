import MessageHandle from "../messageHandle";

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
                // ?????
                // console.log('');
            }
        });
        function generateTxt(str){
            let temp = str.split('\r\n');
            for(let s in temp){
                if(MessageHandle.messageSender) {
                    MessageHandle.messageSender.sendLog(temp[s])
                }
            }
        }
    });
}

