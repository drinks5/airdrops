# encoding: utf-8
import sys
import json
import socket
import os

from django.core.cache import cache
from django.core.management.base import BaseCommand
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()
from apps.contrib import const
from apps.accounts import models
from bots.telegram.client import Client
from bots.utils import TcpClient


class Command(BaseCommand):
    help = '''
    执行客户端命令:
    sendMessage '{"jjj"}'

    '''

    def add_arguments(self, parser):
        """
        python manage.py twitter joinChannel xxxxx --record={name} --iter=1 --mobile=xxxxx
        """
        parser.add_argument('name', help='命令名称')
        parser.add_argument('args', nargs='*')
        parser.add_argument('--mobile', help='指定手机,测试单独某个手机号时打开')
        parser.add_argument('--iter', action='store_true', help="是否逐个发送消息，当遇到需要发送验证码的机器人时打开这个开关")
        parser.add_argument('--record', help="是否需要在Airdrop表插入数据")

    def handle(self, *args, **options):
        pass
