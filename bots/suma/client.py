import logging

import requests
from django.conf import settings

from apps.accounts.models import Config
from bots.utils import logError
logger = logging.getLogger('api')


identify = settings.SU_MA


def Get(url):
    response = ''
    url = url.format(**identify)
    try:
        response = requests.get(url).text
        logger.debug(f'url: {url}')
        logger.debug('response: {}'.format(response))
    except Exception:
        logError()
    return response


def login():
    config = Config.objects.all()
    if config:
        config = config[0]
        if config.suma:
            return config.suma
    else:
        config = Config()
    url = 'http://api.eobzz.com/httpApi.do?action=loginIn&uid={username}&pwd={password}'
    response = Get(url)
    if response.startswith(settings.SU_MA['username']):
        identify['token'] = response
        config.suma = response
        config.save()
        return response
    return ''


identify['token'] = login()


def getUserInfos():
    url = 'http://api.eobzz.com/httpApi.do?action=getUserInfos&uid={username}&token={token}'
    response = Get(url)


def getMobile():
    url = 'http://api.eobzz.com/httpApi.do?action=getMobilenum&pid={projectId}&uid{username}&token={token}&mobile=&size=1'
    response = Get(url)


def start(args, options):
    login()
    getUserInfos()
