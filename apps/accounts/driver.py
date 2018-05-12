import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from .models import Account, AirDrop, Operation

import logging
logger = logging.getLogger('api')
chromedriver = '/Users/mum5/Documents/repo/chromedriver'
textsByField = {
    'email': {
        'items': ['mail']
    },
    'password': {
        'items': ['Password', 'password']
    },
    'lastName': {
        'items': ['Last ']
    },
    'lastName': {
        'items': ['First ']
    },
    'lastName': {
        'items': ['First ']
    },
    'eth': {
        'items': ['Eth', 'Wallet', 'Ethereum']
    },
    'telegram': {
        'items': ['Telegram', 'Username']
    },
    'twitter': {
        'items': ['Twitter']
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


class Driver(object):
    def __init__(self, url: str):
        self.driver = webdriver.Chrome(chromedriver)
        self.driver.get(url)

    def send(self, value: str, elem):
        time.sleep(0.2)
        elem.send_keys(value)
        elem.send_keys(Keys.RETURN)

    def click(self, elem):
        elem.click()

    def locate(self, text: str, method: str = 'find_element_by_xpath'):
        xpath = "//input[contains(@placeholder, '{}')]".format(text)
        method = getattr(self.driver, method)
        try:
            elem = method(xpath)
        except exceptions.NoSuchElementException:
            return
        elem.clear()
        return elem

    def _startField(self, field: str, texts: dict):
        for text in texts['items']:
            elem = self.locate(text)
            if elem:
                self.send(field, elem)
        logger.debug('参数{}: 未匹配'.format(texts['items'][0]))


    def _start(self, account):
        for fieldStr, texts in textsByField.items():
            field= getattr(account, fieldStr, account.name)
            if fieldStr == 'password':
                field = '1qaz2wsx3edcKt!'
            self._startField(field, texts)
        elem = self.locate('recaptcha-checkbox-checkmark',
                           'find_element_by_class_name')
        elem and elem.click()
		

    @classmethod
    def start(cls, name: str, url: str):
        airdrop, ok = AirDrop.objects.get_or_create(name=name, url=url)
        for account in Account.objects.all():
            logger.debug('开始账号{}'.format(account.name))
            cls(url)._start(account)
            Operation.objects.get_or_create(airdrop=airdrop, account=account)
