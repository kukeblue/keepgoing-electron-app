import { app, BrowserWindow, globalShortcut  } from 'electron';
import * as path from 'path';
import messageHandle from './messageHandle'
import { listenLogs } from "./utils/logChangeHandle";
import timer from "./timer"
import MessageHandle from "./messageHandle";
import { Menu } from 'electron'
import { runPyScript, runPyScriptSync } from "./py/runPyScript";



const fs = require("fs");
let mainWindow: Electron.BrowserWindow;
// delete log
fs.truncate('app.log', 0, function () { console.log('clear log success') })

function createWindow(): void {
    Menu.setApplicationMenu(null)
    mainWindow = new BrowserWindow({
        maximizable: false,
        x: 0,
        y: 0,
        icon: path.join(__dirname, 'public/icon/favicon.ico'),
        height: 340,
        webPreferences: {
            // nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js'),
        },
        width: 480,
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

  const ret = globalShortcut.register('CommandOrControl+Q', () => {
    console.log('CommandOrControl+Q is pressed')
    runPyScript('closeAllMhTask', [])
  })
  if (!ret) {
    console.log('registration failed')
  }
}

app.on('ready', createWindow);
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('will-quit', () => {
    // 注销快捷键
    globalShortcut.unregister('CommandOrControl+Q')
   
    // 注销所有快捷键
    globalShortcut.unregisterAll()
  })
app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

