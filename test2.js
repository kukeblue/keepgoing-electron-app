import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
    http.get('https://jingquang.lanh.love/1025/vote');
    sleep(1);
}
// https://cdn.npmmirror.com/binaries/electron/17.4.1/electron-v17.4.1-win32-x64.zip
