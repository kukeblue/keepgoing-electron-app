import { doConnector } from "../client/src/call";

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
    METHOD_CLICK_WATU_MAP: 'method_click_watu_map', // 点击挖图位置
    METHOD_SYNC_IMAGES: 'method_sync_images', // 同步任务图片
    METHOD_BEE_MODE: 'method_bee_mode', // 同步任务图片
    METHOD_ZHUAGUI_TASK: 'method_zhuagui_task',
    METHOD_BUDIAN_TASK: 'method_budian_task',
    METHOD_CLOSE_ALL_TASK: 'method_close_all_task',
    METHOD_THROW_LITTER: 'throw_litter',
    METHOD_SELL_EQUIPMENT: 'sell_equipment',
    METHOD_CONNECTOR: 'method_connector',
    METHOD_ZHANDOU: 'method_zhandou',
    METHOD_HANHUA: 'method_hanhua',
    METHOD_UPDATEPY: 'method_update_py',




    /* *******   主服务消息    ******* */
    MESSAGE_PUSH_LOG: 'message_push_log',
    MESSAGE_PUSH_MAIN_STATE: 'message_push_main_state',
    METHOD_GET_WATU_INFO_REPLY: 'method_get_watu_info_reply', // 返回挖图消息结果


}

export default resourcePaths;
