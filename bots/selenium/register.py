import os

import requests
from django.conf import settings
from faker import Faker

from bots.selenium.base import BaseDriver
from bots.utils import retry
from apps.accounts import models
from apps.contrib import const

ServiceMap = {
    'telegram': {
        'url': 'https://my.telegram.org/auth'
    },
    'eth': {
        'url': 'https://www.myetherwallet.com/'
    },
    'twitter': {
        'url': 'https://twitter.com/i/flow/signup'
    },
    'account': {
        'url': 'https://www.myetherwallet.com/'
    }
}

# Url = 'file:///Users/mum5/Downloads/Authorization.htm'


def register(func):
    ServiceMap[func.__name__.lower()]['callback'] = func
    return func


def getLatestFile(path=settings.MEDIA_ROOT):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


@register
def Account(driver, options):
    faker = Faker()
    profile = faker.profile()
    profile.pop('current_location')
    splitName = profile['name'].split(' ')
    name = ''.join(splitName)
    email = '{}@mum5.cn'.format(name.lower())
    profile['FirstName'], profile['LastName'] = splitName
    if options['update']:
        account = models.Account.objects.get(mobile=options['mobile'])
        account.name = name
        account.profile = profile
        account.email = email
        return account.save()
    eth = Eth(driver, options)
    models.Account.objects.update_or_create(
        email=email,
        mobile=options['mobile'],
        name=name,
        profile=profile,
        zone=options['zone'],
        **eth)
    if settings.MAIL_SERVER:
        requests.get('http://{}/register/{}'.format(settings.MAIL_SERVER,
                                                    account.email))


@register
def Eth(driver, options):
    """
    python manage.py register eth
    """
    ByXpath = driver.driver.find_element_by_xpath
    # 关闭弹窗
    driver.driver.implicitly_wait(3)
    ByXpath('//*[@id="onboardingModal"]/div/div/div/div/img').click()
    ByXpath('/html/body/section[1]/div/main/article[1]/section[1]/div[1]/input'
            ).send_keys(settings.MY_PD)
    # 点击创建钱包
    driver.driver.implicitly_wait(3)
    walletElem = driver.driver.find_element_by_link_text('Create New Wallet')
    retry(walletElem.click)()
    downloadElem = ByXpath(
        "//span[contains(text(), 'Keystore File (UTC / JSON)')]")
    retry(downloadElem.click)()
    driver.driver.implicitly_wait(3)
    with open(getLatestFile(), 'r') as fd:
        json = fd.read()
        eth = '0x' + fd.name.split('--')[-1].split('.')[0]
    #  ByXpath("//span[contains(text(), 'I understand. Continue')]").click()
    #  ByXpath("//span[contains(text(), 'Save Your Address.')]").click()
    print(eth)
    print(json)
    input("输入任意键进入下一个账号")
    return dict(eth=eth, json=json)


@register
def Telegram(driver, options):
    mobile = options['mobile']
    account = models.Account.objects.get(mobile=mobile)
    ByXpath = driver.driver.find_element_by_xpath
    # elem = driver.locate(text='Log Out', method='find_element_by_link_text').click()
    mobileStr = account.zone + mobile
    driver.locate(text='+12223334455').send_keys(mobileStr)
    driver.locate(text="Next", xpath="//button[@type='submit']").click()
    captcha = input("请输入您收到的验证码\n").strip()
    driver.driver.find_element_by_id('my_password').send_keys(captcha)
    #Sign In
    ByXpath('//*[@id="my_login_form"]/div[4]/button').click()
    #API development tools
    driver.driver.implicitly_wait(3)
    driver.driver.find_element_by_link_text('API development tools').click()
    if 'Create' in driver.driver.title:  # Create new application
        ByXpath('//*[@id="app_title"]').send_keys('airdrop')
        ByXpath('//*[@id="app_shortname"]').send_keys('airdrop')
        ByXpath('//*[@id="app_url"]').send_keys('telegram.mum5.cn')
        ByXpath('//*[@id="app_create_form"]/div[4]/div/div[6]/label/input'
                ).click()
        ByXpath('//*[@id="app_save_btn"]').click()
    driver.driver.implicitly_wait(3)
    #api_id
    api_id = ByXpath('//*[@id="app_edit_form"]/div[1]/div[1]/span/strong').text
    api_hash = ByXpath('//*[@id="app_edit_form"]/div[2]/div[1]/span').text
    models.Apis.objects.get_or_create(
        account=account, telegram=dict(api_id=api_id, api_hash=api_hash))
    print('api创建完成')


@register
def Twitter(driver, options):
    account = models.Account.objects.get(mobile=options['mobile'])
    ByXpath = driver.driver.find_element_by_xpath
    # 改用邮箱
    driver.driver.implicitly_wait(3)
    retry(
        ByXpath(
            '//*[@id="react-root"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[4]'
        ).click)()
    # 填写名字
    ByXpath("//input[contains(@placeholder, '{}')]".format('名字')).send_keys(
        account.name)
    ByXpath("//input[contains(@placeholder, '{}')]".format('电子邮件')).send_keys(
        account.email)
    # 下一个
    driver.driver.implicitly_wait(3)
    ByXpath(
        '//*[@id="react-root"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div'
    ).click()
    driver.driver.implicitly_wait(1)
    # 注册
    ByXpath(
        '//*[@id="react-root"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/div'
    ).click()
    # 密码
    driver.driver.implicitly_wait(1)
    ByXpath(
        '//*[@id="react-root"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div[3]/div/div[2]/div/input'
    ).send_keys(settings.TT_PD)
    driver.driver.implicitly_wait(1)
    ByXpath(
        '//*[@id="react-root"]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div'
    ).click()

    # 谷歌验证码
    driver.locate(xpath="//input[@type='submit']").click()
    return driver


def _createTwitterApi(driver, account, ByXpath):
    # application 名称
    driver.driver.get('https://apps.twitter.com/app/new')
    driver.driver.implicitly_wait(5)
    ByXpath('//*[@id="edit-name"]').send_keys('airdrop{}'.format(account.name))
    # application 描述
    ByXpath('//*[@id="edit-description"]').send_keys('airdrop for {}'.format(
        account.name))
    # application 域名
    ByXpath('//*[@id="edit-url"]').send_keys('https://twitter.{}'.format(
        settings.DOMAIN))
    # application 同意勾选
    ByXpath('//*[@id="edit-tos-agreement"]').click()
    # application 点击注册
    ByXpath('//*[@id="edit-submit"]').click()
    driver.driver.implicitly_wait(5)
    # application 点击tab 3
    ByXpath('//*[@id="gaz-content-body"]/div[2]/ul/li[3]/a').click()
    # application 创建token
    ByXpath('//*[@id="edit-submit-owner-token"]').click()

    # application 获取token
    consumer_key = ByXpath(
        '//*[@id="gaz-content-body"]/div[3]/div/div[2]/div[1]/span[2]').text
    consumer_secret = ByXpath(
        '//*[@id="gaz-content-body"]/div[3]/div/div[2]/div[2]/span[2]').text
    access_token_key = ByXpath(
        '//*[@id="gaz-content-body"]/div[3]/div/div[4]/div[1]/span[2]').text
    access_token_secret = ByXpath(
        '//*[@id="gaz-content-body"]/div[3]/div/div[4]/div[2]/span[2]').text
    twitter = dict(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret)
    apis = models.Apis.objects.filter(account=account)
    if not apis:
        models.Apis.objects.create(
            account=account, twitter=twitter, telegram={})
    else:
        apis = apis[0]
        apis.twitter = twitter
        apis.save()


class RegisterDriver(BaseDriver):
    @classmethod
    def start(cls, options):
        service = options['service']
        callback = ServiceMap[service]['callback']
        url = ServiceMap[service]['url']
        driver = cls(url, addCookie=False)
        ByXpath = driver.driver.find_element_by_xpath
        try:
            callback(driver, options)
        except Exception:
            import traceback
            traceback.print_exc()
            import ipdb
            ipdb.set_trace(context=30)
