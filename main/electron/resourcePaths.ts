const resourcePaths = {
    MESSAGE_INIT: 'message_init',
    MESSAGE_INIT_REPLY: 'message_init_replay',



    /* *******   主服务方法    ******* */
    METHOD_START_GAME: 'method_start_game',
    METHOD_START_GAME_REPLY: 'method_start_game_reply',
    METHOD_LOGIN_GAME: 'method_login_game',
    METHOD_LOGIN_GAME_REPLY: 'method_login_game_reply',
    METHOD_TEST: 'method_test',
    METHOD_TEST2: 'method_test2',
    METHOD_KILL_PROCESS: 'method_kill_process',
    METHOD_GET_WATU_INFO: 'method_get_watu_info', // 获取挖图地图消息
    METHOD_SYNC_IMAGES: 'method_sync_images', // 同步任务图片

    /* *******   主服务消息    ******* */
    MESSAGE_PUSH_LOG: 'message_push_log',
    MESSAGE_PUSH_MAIN_STATE: 'message_push_main_state',
    METHOD_GET_WATU_INFO_REPLY: 'method_get_watu_info_reply', // 返回挖图消息结果


}

export default resourcePaths;
