import time
import logging
import multiprocessing

from django.core.management.base import BaseCommand
from faker import Faker

from apps.accounts import models
logger = logging.getLogger('api')


class Command(BaseCommand):
    help = '''创建model '''

    def handle(self, *args, **options):
        create()
        apis()


def apis():
    for data in dataset:
        mobile = data.pop('mobile')
        account = models.Account.objects.get(mobile=mobile)
        models.Apis.objects.get_or_create(telegram=data, account=account)


def create():
    import os
    for data, fileName in zip(dataset, os.listdir('json')):
        faker = Faker()
        with open('json/{}'.format(fileName), 'r') as fd:
            json = fd.read()
            address = '0x' + fileName.split('--')[-1]
            name = faker.name()
            profile = faker.profile()
            profile.pop('current_location')
            models.Account.objects.create(
                email=data['email'],
                name=name,
                eth=address,
                json=json,
                mobile=data['mobile'],
                profile=profile)
