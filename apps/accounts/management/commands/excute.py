# encoding: utf-8
import sys
import json
import socket

from django.core.cache import cache
from django.core.management.base import BaseCommand

from apps.contrib import const
from apps.accounts import models
from bots.client import Client
from bots.utils import TcpClient


class Command(BaseCommand):
    help = '''
    执行客户端命令:
    sendMessage '{"jjj"}'

    '''

    def add_arguments(self, parser):
        parser.add_argument('name', help='命令名称')
        parser.add_argument('args', nargs='*')
        parser.add_argument('--mobile', help='指定手机')
        parser.add_argument('--iter', type=bool)

    def handle(self, *args, **options):
        name = options['name']
        para = args
        if options['iter']:
            parseIter(name, para, options)
            return
        with TcpClient() as client:
            command = getCommand(name=name, para=para)
            client.send(command)


def getCommand(**para):
    return json.dumps(para).encode('utf8')


def parseIter(name, para, options):
    """
    python manage.py excute iter sendMessage xxxx xxxx
    """
    accounts = models.Account.objects.exclude(mobile='').exclude(mobile=None)
    if options['mobile']:
        accounts = accounts.filter(mobile=options['mobile'])
    for account in accounts:
        with TcpClient() as client:
            command = getCommand(
                name='getMessages', para=para, mobile=account.mobile)
            client.send(command)
            texts = client.recv(const.MaxBuffer).decode('utf8')
            print('--------\n')
            print('最近消息:\n{}\n\n'.format(texts, account.mobile))
        reply = input("请输入回复，直接回车则跳过回复\n").format(
            eth=account.eth, email=account.email, name=account.name)
        _para = list(para)
        _para.append(reply)
        command = getCommand(name=name, para=_para, mobile=account.mobile)
        if reply:
            with TcpClient() as client:
                client.send(command)
            print('发送命令{}\n'.format(command))
