import logging
# logging.basicConfig(
#     filename='app.log',
#     level=logging.DEBUG,
#     format=''
# )

logger = logging.getLogger('log_namespace.%s' % 'app')
logger.setLevel(logging.DEBUG)
# usually I keep the LOGGING_DIR defined in some global settings file
file_name = 'app.log'
handler = logging.FileHandler(file_name,  encoding='utf-8')
formatter = logging.Formatter('[%(asctime)s]:[PYTHON]:%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def chLog(message):
    print(message)
    logger.info(message)


if __name__ == '__main__':
    chLog('?????')
