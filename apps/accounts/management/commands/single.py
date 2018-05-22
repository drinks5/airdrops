import time
import logging
import multiprocessing

from django.core.management.base import BaseCommand
from faker import Faker

from apps.accounts import models
from bots.client import Client
logger = logging.getLogger('api')


# class Command(BaseCommand):
    # help = '''单独测试一个account'''

    # def handle(self, *args, **options):
        # client()


def client():
    account = models.Account.objects.get(mobile='18621540168')
    client = Client.create(account)
    return client
