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
    dataset = [{
        'mobile': '1-3239272364',
        'api_id': '242336',
        'api_hash': '8fb82e8c914b17e7f9fe23c3063f6183'
    }, {
        'mobile': '1-3127673166',
        'api_id': '202701',
        'api_hash': '016e2730dc2249a080535f62f0c1f932'
    }, {
        'mobile': '17091930610',
        'api_id': '293174',
        'api_hash': '49eb4c9573626dd03166b0f167265b20'
    }, {
        'mobile': '18621540168',
        'api_id': '289467',
        'api_hash': '3bbbb27babf7141fca8b6b0b8fe1261a'
    }, {
        'mobile': '13106284291',
        'api_id': '248699',
        'api_hash': '05261ab31d0c789d47853aac3b049a5f'
    }, {
        'mobile': '18817403149',
        'api_id': '208252',
        'api_hash': '7f972c6a88b8da3f91a3dc910b0810ea'
    }, {
        'mobile': '1-7853630580',
        'api_id': '222268',
        'api_hash': 'b1d68b71be18e1b6178cc6ddf66e672e'
    }, {
        'mobile': '1-8059960386',
        'api_id': '244138',
        'api_hash': 'd4f2f68cb483525356e0769edbfa251b'
    }, {
        'mobile': '13074697745',
        'api_id': '297977',
        'api_hash': '2eb06427536a3adbccdfdb4edb7bd804'
    }]
    for data in dataset:
        mobile = data.pop('mobile')
        account = models.Account.objects.get(mobile=mobile)
        models.Apis.objects.get_or_create(telegram=data, account=account)


def create():
    import os
    dataset = [{
        'mobile': '',
        'email': ''
    }, {
        'mobile': '',
        'email': ''
    }, {
        'mobile': '',
        'email': ''
    }, {
        'mobile': '',
        'email': ''
    }, {
        'mobile': '13074697745',
        'email': 'drink.sobest@gmail.com'
    }, {
        'mobile': '1-8059960386',
        'email': 'davidlucero@mum5.cn'
    }, {
        'mobile': '1-7853630580',
        'email': 'annaramirez@mum5.cn'
    }, {
        'mobile': '18817403149',
        'email': 'mm@mum5.cn'
    }, {
        'mobile': '13106284291',
        'email': 'ss@mum5.cn'
    }, {
        'mobile': '18621540168',
        'email': 'me@mum5.cn'
    }, {
        'mobile': '17091930610',
        'email': 'drinksober@foxmail.com'
    }, {
        'mobile': '1-3127673166',
        'email': 'dalewilson@mum5.cn'
    }, {
        'mobile': '1-3239272364',
        'email': 'scottmacdonald@mum5.cn'
    }]
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
