import urllib
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from apps.accounts.models import Account, AirDrop, Operation
from .base import BaseDriver
from .utils import logError

import logging
logger = logging.getLogger('api')
textsByField = {
    'email': {
        'items': ['mail', '邮箱']
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
        'items': ['Eth', 'Wallet', 'Ethereum', '钱包']
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


class Driver(BaseDriver):

    def _startField(self, field: str, texts: dict):
        for text in texts['items']:
            self.locate(text=text).send_keys(field)
        logger.debug('参数{}: 未匹配'.format(texts['items'][0]))

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
    def start(cls, name: str = '', url: str = ''):
        if name:
            airdrop = AirDrop.objects.filter(name=name.lower())
            if airdrop:
                airdrop = airdrop[0]
            else:
                airdrop = AirDrop.objects.create(name=name.lower(), url=url)
        #  url = 'file:///Users/mum5/Downloads/RusGas.htm'
        for index, account in enumerate(Account.objects.exclude(email='')):
            logger.debug('开始第{}账号:\n{}'.format(index, account))
            driver = cls(url)
            try:
                driver._start(account)
                finished = input()
            finally:
                try:
                    driver.driver.close()
                except:
                    pass
            if finished is not None and name:
                operation, ok = Operation.objects.get_or_create(
                    airdrop=airdrop, account=account)
                if not ok:
                    logger.debug('该账号已经操作过此空投')
        logger.debug('完成全部账号')
