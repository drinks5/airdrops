import time
import logging
import multiprocessing

from django.core.management.base import BaseCommand
from faker import Faker

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
    for account in accounts:
        client = Client(account)
        multiprocessing.Process(target=client.forever).start()
    while True:
        time.sleep(0.5)
