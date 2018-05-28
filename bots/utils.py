import logging
from traceback import format_exc
import random
import time
import json
import socket

from apps.contrib import const

logger = logging.getLogger('api')


def logError():
    logger.error(format_exc())


class TcpClient(object):
    client = None

    def __enter__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(True)
        self.client.connect(const.Tcp)
        return self.client

    def __exit__(self, *args):
        self.client.close()


class Chat:
    username = ''
    phone = ''


class Event(object):
    def __init__(self, bytes):
        self.raw_text = bytes.decode('utf8')
        self.chat = Chat()
        try:
            self.json = json.loads(self.raw_text)
        except (TypeError, ValueError):
            self.json = {}

    def __str__(self):
        return self.raw_text

    __repr__ = __str__


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
        self.target = data.get('target', '')
        self.mobile = data.pop('mobile', '')
        self.msg = self.para and self.para[0] or ''

    def __str__(self):
        return '<Command {}: {}, {}>'.format(self.name, self.target, self.para)

    __repr__ = __str__


def sleep():
    num = random.randint(1, 10) * random.random()
    logger.debug('sleep {}'.format(num))
    time.sleep(num)
