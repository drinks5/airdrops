import logging

from django.core.management.base import BaseCommand

from bots.selenium.register import RegisterDriver as Driver
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''开始填写表单'''

    def add_arguments(self, parser):
        parser.add_argument('service', help='服务，telegram或eth')
        parser.add_argument('--mobile', help='手机号')
        parser.add_argument('--update', help='是否更新', action="store_true")
        parser.add_argument('--zone', help='zone字段,如--zone=+1', default='+86')

    def handle(self, *args, **options):
        try:
            driver(options)
        except KeyboardInterrupt:
            pass


def driver(options):
    Driver.start(options)
