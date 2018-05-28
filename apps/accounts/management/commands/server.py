import time
import logging
import socket
import threading

from django.core.management.base import BaseCommand

from apps.accounts import models
from apps.contrib import const
from bots.client import Client
from bots.utils import Event
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''开始填写表单'''

    def add_arguments(self, parser):
        parser.add_argument('--mobile', help='手机号', default='')

    def handle(self, *args, **options):
        try:
            main(options)
        except KeyboardInterrupt:
            pass


def main(options):
    accounts = models.Account.objects.all().select_related('apis')
    mobile = options.get('mobile')
    if mobile:
        accounts = models.Account.objects.filter(mobile=mobile)
    clients = Client.bulkCreate(accounts)
    server(clients)


def handle_client_connection(client_socket, clients):
    request = client_socket.recv(1024)
    event = Event(request)
    if event.json.get('mobile'):
        clients = [
            x for x in clients if x.account.mobile == event.json['mobile']
        ]
    for client in clients:
        client.instance.get_dialogs()
        logger.debug('{}发送命令:{}'.format(client.account.mobile, event))
        response = client.OnMessage(event) or 'ok'
        try:
            client_socket.send(response.encode('utf8'))
        except BrokenPipeError:
            # 客户端连接已经关闭
            if response != 'ok':
                logger.debug('发送失败:{}'.format(response.encode('utf8')))
    client_socket.close()
    logger.debug('全部客户端命令发送完成')


def server(clients):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(const.Tcp)
    server.listen(5)  # max backlog of connections
    try:
        mainLoop(clients, server)
    finally:
        server.close()


def mainLoop(clients, server):
    while True:
        time.sleep(0.5)
        client_sock, address = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection, args=(client_sock, clients))
        client_handler.start()
