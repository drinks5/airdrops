import logging

from django.core.management.base import BaseCommand
from bots.telegram.client import Client
from bots.utils import Command as MyCommand, TcpClient

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
        name = options['name']
        para = list(args)
        target = ''
        if para:
            target = para.pop(0)
        with TcpClient() as client:
            command = MyCommand.from_dict(
                name=name, para=para, target=target,
                mobile=options['mobile']).to_bytes()
            client.send(command)
