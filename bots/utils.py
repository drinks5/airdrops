import logging
from traceback import format_exc
import random
import time
import json

logger = logging.getLogger('api')


def logError():
    logger.error(format_exc())


def retry(func):
    count = 0

    def inner(*args):
        while True:
            try:
                return func(*args)
            except Exception:
                count += 1
            if count == 3:
                logError()
                break

    return inner


class Command(object):
    def __init__(self, text):
        try:
            data = json.loads(text)
        except (ValueError, TypeError):
            data = {}

        self.raw_text = text
        self.name = data.pop('name', '')
        self.para = data.pop('para', [])
        self.mobile = data.pop('mobile', '')

    def __str__(self):
        return '<Command: {}, {}>'.format(self.name, self.para)

    __repr__ = __str__


def sleep():
    num = random.randint(1, 10) * random.random()
    logger.debug('sleep {}'.format(num))
    time.sleep(num)
