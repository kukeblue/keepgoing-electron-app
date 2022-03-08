import { app, BrowserWindow } from 'electron';
const electronReload = require('electron-reload')
import * as path from 'path';
import MessageHadle from './messageHandle'
let mainWindow: Electron.BrowserWindow;

function createWindow(): void {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        x: 0,
        y: 0,
        icon: path.join(__dirname, 'public/icon/favicon.ico'),
        height: 800,
        webPreferences: {
            // nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js'),
        },
        width: 1200,
    });
    // and load the index.html of the app.
    mainWindow.loadFile(path.join(__dirname, '../html/index.html'));
    // Open the DevTools.
    // Emitted when the window is closed.
    mainWindow.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    });
}
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);
// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On OS X it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
app.on('activate', () => {
    // On OS X it"s common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) {
        createWindow();
    }
});

MessageHadle.init()