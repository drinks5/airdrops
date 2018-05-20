import time
import logging
import multiprocessing

from django.core.management.base import BaseCommand
from faker import Faker

from apps.accounts import models
from bots.client import Client
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''逐行遍历account'''


    def add_arguments(self, parser):
        parser.add_argument('name', help='代币名称')
        parser.add_argument('url', help='url')

    def handle(self, *args, **options):
        accounts = models.Account.objects.exclude(email='')
        airdrop, ok = models.AirDrop.objects.get_or_create(name=options['name'], url=options['url'])
        for account in accounts:
            print(account)
            models.Operation.objects.get_or_create(account=account, airdrop=airdrop)
            input()
