# encoding: utf-8
import sys
import json
import socket

from django.core.cache import cache
from django.core.management.base import BaseCommand

from apps.contrib import const
from apps.accounts import models
from bots.telegram.client import Client
from bots.utils import TcpClient, Command as MyCommand


class Command(BaseCommand):
    help = '''
    执行客户端命令:
    sendMessage '{"jjj"}'

    '''

    def add_arguments(self, parser):
        """
        python manage.py excute joinChannel xxxxx --record={name} --iter=1 --mobile=xxxxx
        """
        parser.add_argument('name', help='命令名称')
        parser.add_argument('args', nargs='*')
        parser.add_argument('--mobile', help='指定手机,测试单独某个手机号时打开')
        parser.add_argument('--iter', action='store_true', help="是否逐个发送消息，当遇到需要发送验证码的机器人时打开这个开关")
        parser.add_argument('--record', help="是否需要在Airdrop表插入数据")

    def handle(self, *args, **options):
        name = options['name']
        para = list(args)
        target = ''
        if para:
            target = para.pop(0)
        if options['record']:
            models.AirDrop.objects.get_or_create(
                name=options['record'], url=para[0])
        if options['iter']:
            parseIter(name, target, para, options)
            return
        with TcpClient() as client:
            command = MyCommand.from_dict(name=name, para=para, target=target).to_bytes()
            client.send(command)


def getCommand(**para):
    return json.dumps(para).encode('utf8')


def parseIter(name, target, para, options):
    """
    python manage.py excute iter sendMessage xxxx xxxx
    """
    accounts = models.Account.objects.exclude(mobile='').exclude(mobile=None)
    if options['mobile']:
        accounts = accounts.filter(mobile=options['mobile'])
    for account in accounts:
        with TcpClient() as client:
            command = getCommand(
                name='getMessages',
                target=target,
                para=para,
                mobile=account.mobile)
            client.send(command)
            texts = client.recv(const.MaxBuffer).decode('utf8')
        print('--------\n')
        print('最近消息:\n{}\n\n{}'.format(texts, account.mobile))
        reply = input("请输入回复，直接回车则跳过回复\n")
        _para = list(para)
        _para.append(reply)
        _para = [
            x.format(eth=account.eth, email=account.email, name=account.name)
            for x in _para
        ]
        command = getCommand(
            name=name, para=_para, mobile=account.mobile, target=target)
        if reply:
            with TcpClient() as client:
                client.send(command)
                print('发送命令{}\n'.format(command))
