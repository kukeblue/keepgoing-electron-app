import logging
import sys
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
 )

if __name__ == '__main__':
    logging.debug("I am written to the file")
