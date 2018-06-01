import time
import threading

from apps.contrib import const
from apps.accounts.models import Account, AirDrop, Operation
from .base import BaseDriver
from bots.utils import logError

import logging
logger = logging.getLogger('api')
NAMES = [
    'facebook_username', 'name', 'Name', 'Username', 'username',
    'telegram_username', 'Twitter', 'Telegram', 'twitter_username', 'twitter'
]
textsByField = {
    'email': {
        'items': ['mail', '邮箱', 'Email', 'email']
    },
    'mobile': {
        'items': ['Mobile', 'mobile', '手机', 'phone']
    },
    'password': {
        'items': ['Password', 'password', '密码']
    },
    'password2': {
        'items': ['Password', 'password', '密码', 'password2']
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
            if self.locate(
                    text=text, xpath="//input[@id='{}']").send_keys(field):
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
                except Exception:
                    logError()

    @classmethod
    def start(cls, options):
        name = options['name'].lower()
        url = options['url']
        airdrop = AirDrop.objects.filter(name=name)
        if airdrop:
            airdrop = airdrop[0]
        else:
            airdrop = AirDrop.objects.create(name=name, url=url)
        #  url = 'file:///Users/mum5/Downloads/RusGas.htm'
        accounts = Account.objects.exclude(email='')
        if options['mobile']:
            accounts = accounts.filter(mobile=options['mobile'])
        accounts = list(accounts)
        drivers = []

        for item in accounts[::const.MaxWindow]:
            for i in range(int(len(accounts) / const.MaxWindow)):
                index = accounts.index(item) + i
                if index < len(accounts):
                    #  _startOne(cls, url, account)
                    driver = driver(url)
                    drivers.append(driver)
                    account = accounts[index]
                    threading.Thread(
                        target=_startOne, args=(driver, url, account)).start()
                    operation, ok = Operation.objects.get_or_create(
                        airdrop=airdrop, account=account)
                    if not ok:
                        logger.debug('该账号已经操作过此空投')
            input("输入任意键进入一下队列")
            for driver in drivers:
                driver.driver.close()
        logger.debug('完成全部账号')


def _startOne(driver, url, account):
    logger.debug('开始账号:\n{}'.format(account))
    try:
        driver._start(account)
    except Exception:
        pass
    time.sleep(2 * 60)
