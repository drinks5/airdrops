# encoding: utf-8
from django.core.management.base import BaseCommand

from bots.mailserver.dog import watchDog


class Command(BaseCommand):
    help = '''
    watch dog 监听邮件
    '''

    def handle(self, *args, **options):
        watchDog()
