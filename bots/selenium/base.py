import time
import logging

from django.conf import settings
from selenium import webdriver
from selenium.common import exceptions

from apps.contrib import const
from bots.selenium.proxy import create_proxyauth_extension
from bots.utils import logError
logger = logging.getLogger('api')
proxyConfig = settings.PROXY_SERVER
chromedriver = '/Users/mum5/Documents/repo/chromedriver'
geckodriver = '/usr/local/bin/geckodriver'


class Element(object):
    def __init__(self, elem=None):
        self.elem = elem

    def send_keys(self, value):
        if not self.elem:
            return self

        time.sleep(0.2)
        try:
            logger.debug('发送值:{}'.format(value))
            self.elem.clear()
            self.elem.send_keys(value)
        except exceptions.InvalidElementStateException:
            pass
        return self

    def click(self):
        time.sleep(0.2)
        try:
            self.elem and self.elem.click()
        except exceptions.InvalidElementStateException:
            pass
        return self

    def clear(self):
        try:
            self.elem and self.elem.clear()
        except exceptions.InvalidElementStateException:
            pass
        return self

    def __nonzero__(self):
        return bool(self.elem)

    __bool__ = __nonzero__

    def __str__(self):
        return str(self.elem)

    __repr__ = __str__


class Wait(object):
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        self.driver.implicitly_wait(1)

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass


def getProxy():
    from selenium.webdriver.common.proxy import Proxy
    return Proxy(getProxyMap())


def getProxyMap():
    from selenium.webdriver.common.proxy import ProxyType
    proxy = {
        'proxyType': ProxyType.MANUAL,
        'httpProxy': proxyConfig['host'],
        'sslProxy': proxyConfig['host'],
        'ftpProxy': proxyConfig['host'],
        'socksProxy': proxyConfig['host'],
        'noProxy': '',
        'socksUsername': proxyConfig['username'],
        'socksPassword': proxyConfig['password'],
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }
    return proxy


def getFirefoxDriver():
    from base64 import b64encode
    profile = webdriver.FirefoxProfile()
    username = proxyConfig['username']
    password = proxyConfig['password']
    credentials = f'{username}:{password}'
    credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
    profile.set_preference('extensions.closeproxyauth.authtoken', credentials)
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.share_proxy_settings", True)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("network.proxy.http", proxyConfig['host'])
    profile.set_preference("network.proxy.http_port", proxyConfig['port'])
    profile.set_preference('network.proxy.ssl_port', proxyConfig['port'])
    profile.set_preference('network.proxy.ssl', proxyConfig['host'])
    profile.set_preference("general.useragent.override", "whater_useragent")
    profile.update_preferences()
    browser = webdriver.Firefox(firefox_profile=profile)
    return browser


def getChromeDriver():
    chromeOptions = webdriver.ChromeOptions()
    desired_capabilities = chromeOptions.to_capabilities()
    proxyPlugin = create_proxyauth_extension(**settings.PROXY_SERVER)
    chromeOptions.add_extension(proxyPlugin)
    preferences = {
        "download.default_directory": settings.MEDIA_ROOT,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chromeOptions.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(
        chrome_options=chromeOptions,
        executable_path=chromedriver,
        desired_capabilities=desired_capabilities)
    return driver


class BaseDriver(object):
    def __init__(self, url: str, addCookie=True) -> None:

        driver = getChromeDriver()

        self.driver = driver
        self.driver.get(url)

        self.wait = Wait(driver)
        if url.startswith('file'):
            addCookie = False
        for key, value in const.RecaptchaCookie.items():
            try:
                addCookie and driver.add_cookie({
                    'name': key,
                    'value': value,
                    'domain': '.google.com',
                    'path': '/'
                })
            except exceptions.WebDriverException:
                pass

    def locate(self,
               text: str = '',
               method: str = 'find_element_by_xpath',
               xpath="//input[contains(@placeholder, '{}')]"):
        xpath = xpath.format(text)
        method = getattr(self.driver, method)
        elem = Element()
        try:
            elem = Element(method(xpath))
        except exceptions.NoSuchElementException:
            pass
        return elem
