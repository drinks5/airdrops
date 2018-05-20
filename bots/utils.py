import logging
from traceback import format_exc
import random
import time

logger = logging.getLogger('api')


def logError():
    logger.error(format_exc())


class Command(object):
    def __init__(self, text):
        tuples = text.split(' ')  # '/joinGroup https://xxx.com'
        self.name = tuples[0].strip('/')
        self.para = tuples[1:]

    def __str__(self):
        return '<Command: {}, {}>'.format(self.name, self.para)

    __repr__ = __str__

def sleep():
    num = random.randint(1, 10) * random.random()
    logger.debug('sleep {}'.format(num))
    time.sleep(num)

