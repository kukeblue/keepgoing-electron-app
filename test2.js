import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
    http.get('https://jingquang.lanh.love/1025/vote');
    sleep(1);
}