import time
import logging
import socket
import threading

from django.core.management.base import BaseCommand

from apps.accounts import models
from bots.client import Client
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''开始填写表单'''

    def add_arguments(self, parser):
        parser.add_argument('-index', help='代币名称', default='')

    def handle(self, *args, **options):
        try:
            main(options)
        except KeyboardInterrupt:
            pass


def main(options):
    accounts = models.Account.objects.exclude(email='')
    index = options.get('index')
    if index:
        account = accounts[int(index)]
        print(account)
        Client(account).forever()
        return
    clients = Client.bulkCreate(accounts)
    server(clients)


class Event(object):
    def __init__(self, bytes):
        self.raw_text = bytes.decode('utf8')


def handle_client_connection(client_socket, clients):
    request = client_socket.recv(1024)
    event = Event(request)
    for client in clients:
        client.OnMessage(event)
        time.sleep(30)
    client_socket.close()


def server(clients):
    bind_ip = '0.0.0.0'
    bind_port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(
                client_sock, clients
            )  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        )
        client_handler.start()
