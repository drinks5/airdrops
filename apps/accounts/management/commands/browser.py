import time
import logging
import multiprocessing

from django.core.management.base import BaseCommand
from faker import Faker

from apps.accounts import models
from bots.client import Client
from bots.browser import Driver
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''开始填写表单'''

    def add_arguments(self, parser):
        parser.add_argument('name', help='代币名称')
        parser.add_argument('url', help='url')

    def handle(self, *args, **options):
        try:
            driver(options)
        except KeyboardInterrupt:
            pass


def driver(options):
    Driver.start(options['name'], options['url'])
