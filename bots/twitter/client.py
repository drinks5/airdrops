import time
import logging

from django.conf import settings
import twitter

logger = logging.getLogger('api')


def get_proxys():
    host = settings.PROXY_SERVER['host']
    port = settings.PROXY_SERVER['port']
    username = settings.PROXY_SERVER['username']
    password = settings.PROXY_SERVER['password']
    proxies = {
        'http': f'http://{username}:{password}@{host}:{port}',
        'https': f'http://{username}:{password}@{host}:{port}'
    }
    return proxies


class Client(object):
    def __init__(self, account):
        proxies = get_proxys()
        self.api = twitter.Api(proxies=proxies, **account.twitter.api)
        user = self.api.VerifyCredentials()
        self.id = user.id
        self.screen_name = user.screen_name

    @classmethod
    def create(cls, account, index=''):
        return cls(account)

    @classmethod
    def bulkCreate(cls, accounts):
        clients = []
        for index, account in enumerate(accounts):
            if account.twitter.api:
                clients.append(cls.create(account, index))
            time.sleep(0.2)
        logger.debug('初始化完成推特客户端: {}个'.format(len(accounts)))
        return clients

    def send_message(self, message):
        status = self.api.PostUpdate(message)
        return True if status.text == message else False

    def like(self, target, follow=True):
        if target.isdigit():
            return self.api.CreateFriendship(user_id=id, follow=follow)
        return self.api.CreateFriendship(screen_name=target, follow=follow)

    def dislike(self, id=None, screen_name=None):
        self.like(self, id, screen_name, False)

    def get_friend_IDs(self):
        return self.api.GetFriendIDs()
