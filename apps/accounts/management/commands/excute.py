# encoding: utf-8
import sys
import json
import socket
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '''执行客户端命令'''

    def add_arguments(self, parser):
        parser.add_argument('name', help='命令名称')
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('0.0.0.0', 9999))
        name = options['name']
        para = args
        command = json.dumps(dict(name=name, para=para)).encode('utf8')
        try:
            json.loads(name)
            command = name
        except (TypeError, ValueError):
            pass
        client.send(command)
