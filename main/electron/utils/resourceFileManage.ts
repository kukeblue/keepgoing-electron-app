import { existsSync } from 'fs';
const http = require("http")
const path = require("path");
const fs = require("fs");

function syncServeImages(userDir: string, remoteFiles) {
    const sourceDir = path.join(__dirname, `../py/config/images/${userDir}/`)
    if(!existsSync(sourceDir)) {
        fs.mkdirSync(sourceDir)
    }
    const files = fs.readdirSync(sourceDir)
    remoteFiles.forEach((fileName: string)=>{
        if(!files.includes(fileName)) {
            const cf = sourceDir + fileName
            download('http://kuke-static.kukechen.top/WechatIMG9.png', cf)
        }
    })
}

const download = function(url: string, dest: string, cb?: Function) {
    let file = fs.createWriteStream(dest);
    let request = http.get(url, function(response) {
        response.pipe(file);
        file.on('finish', function() {
            console.log('file download success')
            file.close(cb);  // close() is async, call cb after close completes.
        });
    }).on('error', function(err) { // Handle errors
        fs.unlink(dest); // Delete the file async. (But we don't check the result)
        if (cb) cb(err.message);
    });
};





