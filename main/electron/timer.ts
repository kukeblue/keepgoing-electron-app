

let timerSecondCallbacks = []
let intervalPid:any = null

function initTimer(option:{
    secondCallbacks: Function[] // 秒级执行器
}) {
    timerSecondCallbacks = option.secondCallbacks
    // 每秒执行器
    intervalPid = setInterval(() => {
        timerSecondCallbacks.forEach((callback)=>{
            callback()
        })
    }, 1000);
}

export default {
    intervalPid,
    timerSecondCallbacks,
    initTimer
}
