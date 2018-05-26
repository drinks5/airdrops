import time

from django.conf import settings
from selenium import webdriver
from selenium.common import exceptions

from apps.contrib import const
chromedriver = '/Users/mum5/Documents/repo/chromedriver'


class Element(object):
    def __init__(self, elem=None):
        self.elem = elem

    def send_keys(self, value):
        time.sleep(0.2)
        self.elem and self.elem.send_keys(value)
        return self

    def click(self):
        time.sleep(0.2)
        self.elem and self.elem.click()
        return self

    def clear(self):
        self.elem and self.elem.clear()
        return self

    def __str__(self):
        return str(self.elem)

    __repr__ = __str__


class Wait(object):
    def __init__(self, driver):
        self.driver = driver

    def __enter__(self):
        driver.implicitly_wait(1)

    def __exit__(self, exc_type, exc_value, exc_tb):
        pass


class BaseDriver(object):
    def __init__(self, url: str, addCookie=True):
        chrome_options = webdriver.ChromeOptions()
        preferences = {
            "download.default_directory": settings.MEDIA_ROOT,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", preferences)
        driver = webdriver.Chrome(
            chrome_options=chrome_options, executable_path=chromedriver)
        self.driver = driver
        self.driver.get(url)

        self.wait = Wait(driver)
        if url.startswith('file'):
            addCookie = False
        for key, value in const.RecaptchaCookie.items():
            addCookie and driver.add_cookie({
                'name': key,
                'value': value,
                'domain': '.google.com',
                'path': '/'
            })

    def locate(self,
               text: str,
               method: str = 'find_element_by_xpath',
               xpath="//input[contains(@placeholder, '{}')]"):
        xpath = xpath.format(text)
        method = getattr(self.driver, method)
        elem = Element()
        try:
            elem = Element(method(xpath))
        except exceptions.NoSuchElementException:
            pass
        'input' in xpath and elem.clear()
        return elem
