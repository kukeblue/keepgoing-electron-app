import { configure, getLogger } from "log4js";


configure({
    appenders: { appLog: { type: "file", filename: "app.log" }, out: { type: 'stdout' }, },
    categories: { default: { appenders: ["appLog", "out"], level: "debug" } }
});

export const logger = getLogger("appLog");


