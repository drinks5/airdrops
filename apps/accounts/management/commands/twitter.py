import logging

from django.core.management.base import BaseCommand

from apps.accounts import models
from bots.twitter.client import Client

logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''
    执行客户端命令:
    like xxxx                   关注用户xxx
    sendMessage xxxxx           发送推特xxxx
    forward     xxxx    xxxx    转发推特xxx,转发内容xxx
    dislike     xxxx            取关用户xxxx
    '''

    def add_arguments(self, parser):
        parser.add_argument('name', help='命令名字')
        parser.add_argument('args', nargs='*')
        parser.add_argument('--mobile', help='指定手机号')

    def handle(self, *args, **options):
        accounts = models.Account.objects.filter()
        if options['mobile']:
            accounts = accounts.filter(mobile=options['mobile'])
        clients = Client.bulkCreate(accounts)
        for client in clients:
            method = getattr(client, options['name'])
            method(*args)
