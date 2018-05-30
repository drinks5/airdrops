import urllib
import time
from itertools import zip_longest
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from apps.accounts.models import Account, AirDrop, Operation
from .base import BaseDriver
from bots.utils import logError

import logging
logger = logging.getLogger('api')
NAMES = [
    'facebook_username', 'name', 'Name', 'Username', 'username',
    'telegram_username', 'Twitter', 'Telegram', 'twitter_username',
    'twitter'
]
textsByField = {
    'email': {
        'items': ['mail', '邮箱', 'Email', 'email']
    },
    'mobile': {
        'items': ['Mobile', 'mobile', '手机']
    },
    'password': {
        'items': ['Password', 'password', '密码']
    },
    'passwordConfirm': {
        'items': ['Password', 'password', '密码']
    },
    'lastName': {
        'items': ['Last ']
    },
    'FirstName': {
        'items': ['First ']
    },
    'eth': {
        'items': ['Eth', 'Wallet', 'Ethereum', '钱包', 'eth_address']
    },
    'name': {
        'items': NAMES
    },
    'facebook': {
        'items': NAMES
    },
    'telegram': {
        'items': NAMES
    },
    'twitter': {
        'items': NAMES
    },
    # 'accept': {
    # 'items': ['Accept'],
    # 'type': 'button'
    # },
    # 'service': {
    # 'items': ['Understand', 'understand'],
    # 'type': 'button'
    # }
}


def send_keys(elem, field):
    pass


class Driver(BaseDriver):
    def _startField(self, field: str, texts: dict):
        for text in texts['items']:
            if self.locate(
                    text=text,
                    xpath="//input[contains(@placeholder, '{}')]").send_keys(
                        field):
                return
            if self.locate(
                    text=text, xpath="//input[@type='{}']").send_keys(field):
                return
            if self.locate(
                    text=text, xpath="//input[@name='{}']").send_keys(field):
                return

    def _start(self, account):
        for fieldStr, texts in textsByField.items():
            field = getattr(account, fieldStr, account.name)
            if 'password' in fieldStr:
                field = '1qaz2wsx3edcKt!'
            self._startField(field, texts)
        checkboxs = self.driver.find_elements_by_xpath(
            "//input[@type='checkbox']")
        for checkbox in checkboxs:
            if not checkbox.is_selected():
                try:
                    checkbox.click()
                except:
                    logError()

    @classmethod
    def start(cls, options):
        name = options['name'].lower()
        url = options['url']
        finished = ''
        airdrop = AirDrop.objects.filter(name=name)
        if airdrop:
            airdrop = airdrop[0]
        else:
            airdrop = AirDrop.objects.create(name=name, url=url)
        #  url = 'file:///Users/mum5/Downloads/RusGas.htm'
        accounts = Account.objects.exclude(email='')
        if options['mobile']:
            accounts = accounts.filter(mobile=options['mobile'])
        for account in accounts[:4]:
            _startOne(cls, url, account)
            #  threading.Thread(
                #  target=_startOne, args=(cls, url, account)).start()
            operation, ok = Operation.objects.get_or_create(
                airdrop=airdrop, account=account)
            if not ok:
                logger.debug('该账号已经操作过此空投')
        logger.debug('完成全部账号')


def _startOne(cls, url, account):
    driver = cls(url)
    logger.debug('开始账号:\n{}'.format(account))
    try:
        driver._start(account)
    except Exception:
        pass
    time.sleep(2 * 60)
