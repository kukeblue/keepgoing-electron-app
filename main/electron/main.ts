import { app, BrowserWindow } from 'electron';
import * as path from 'path';
import messageHandle from './messageHandle'
import { listenLogs } from "./utils/logChangeHandle";
import timer from "./timer"
import MessageHandle from "./messageHandle";
const fs = require("fs");
let mainWindow: Electron.BrowserWindow;

// delete log
fs.truncate('app.log', 0, function () { console.log('clear log success') })

function createWindow(): void {
    mainWindow = new BrowserWindow({
        x: 0,
        y: 0,
        icon: path.join(__dirname, 'public/icon/favicon.ico'),
        height: 750,
        webPreferences: {
            // nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js'),
        },
        width: 900,
    });
    mainWindow.loadFile(path.join(__dirname, '../../html/index.html'));
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
    messageHandle.init(mainWindow)
    timer.initTimer({
        secondCallbacks: [MessageHandle.messageSender.sendState]
    })
    listenLogs('app.log')
}

app.on('ready', createWindow);
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

