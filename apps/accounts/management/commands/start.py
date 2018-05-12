from django.core.management.base import BaseCommand
from account.driver import Driver


class Command(BaseCommand):
    help = '''开始填写表单'''
    def add_arguments(self, parser):
        parser.add_argument('name', help='代币名称')
        parser.add_argument('url', help='url')

    def handle(self, *args, **options):
        Driver.start(options['name'], options['url'])
        input('输入任意键退出')
