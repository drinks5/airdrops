# encoding: utf-8

import logging
import time
import datetime

import telethon
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from faker import Faker
from django.conf import settings

from apps.contrib import const
from bots.utils import logError, Command, sleep

logger = logging.getLogger('api')


class Dispatch(object):
    client = None

    def __init__(self, client):
        self.client = client

    def joinMyChannel(self):
        if self.client.account.profile.get('joinedMyChannel'):
            return
        try:
            self.client.instance(ImportChatInviteRequest(settings.MY_CHANNEL))
            self.client.account.profile['joinedMyChannel'] = True
        except telethon.errors.rpc_error_list.UserAlreadyParticipantError:
            self.client.account.profile['joinedMyChannel'] = True
            pass
        except Exception:
            logError()
        self.client.account.save()

    def joinChannel(self, command):
        time.sleep(10)
        logger.debug('start command joinChannel {}'.format(command))
        try:
            group = self.client.instance.get_entity(command.target)
            self.client.instance(JoinChannelRequest(group))
            self.client.account.save()
            logger.debug('finish command joinChannel')
        except Exception:
            logError()

    def sendMessage(self, command):
        time.sleep(1)
        account = self.client.account
        self.client.instance.send_message(command.target,
                                          command.msg.format(
                                              eth=account.eth,
                                              email=account.email,
                                              name=account.name))

    def updateUsername(self, command):
        if self.client.account.profile.get('updatedUsername'):
            return
        me = self.client.instance.get_me()
        origiUsername = me.username
        if me.username:
            logger.debug('username为{}，无须更新'.format(origiUsername))
            return
        while True:
            faker = Faker()
            username = faker.name()
            username = ''.join(username.split(' '))
            try:
                logger.debug('updateUsername {}\n原始username为:{}\n'.format(
                    username, origiUsername))
                self.client.instance(UpdateUsernameRequest(username))
                self.client.account.name = username
                self.client.account.profile['updatedUsername'] = True
                self.client.account.save()
                logger.debug('完成更新usernmae{}'.format(username))
                return
            except Exception:
                logError()
            time.sleep(10)

    def excute(self, command):
        method = getattr(self, command.name, None)
        if not method:
            return
        return method(command)

    def getMessages(self, command):
        """
        getMessages https://t.me/FanfareAirdropBot
        """
        now = datetime.datetime.now()
        entity = command.target
        messages = sorted(
            self.client.instance.get_messages(
                entity, offset_date=now, limit=5),
            key=lambda x: x.id)
        return '\n-----\n'.join(
            ['{}: {}'.format(x.date, x.message) for x in messages])


class Client(object):
    def __init__(self, account):
        self.account = account
        telegram = self.account.apis.telegram
        api_id = telegram['api_id']
        api_hash = telegram['api_hash']
        self.instance = TelegramClient(
            self.account.name,
            api_id,
            api_hash,
            proxy=const.Proxy,
            update_workers=4,
            spawn_read_thread=True)
        self.dispatch = Dispatch(self)

    def OnMessage(self, event):
        command = Command(event.raw_text)
        if command.mobile and command.mobile != self.account.mobile:  # 如果命令中指定手机号，则在指定手机号中执行命令
            return
        if str(event.chat.phone) == const.TelegramPhone:
            logger.debug('{}: {}'.format(self.account.mobile, event.raw_text))
        try:
            return self.dispatch.excute(command)
        except Exception:
            logError()
        return ''

    @classmethod
    def create(cls, account, index=''):
        self = cls(account)
        if index:
            index = '第{}个账号'.format(index)
        logger.debug('开始登陆:\n{}'.format(self.account, index))
        self.instance.start()
        self.dispatch.joinMyChannel()
        self.instance.on(events.NewMessage)(self.OnMessage)
        logger.debug('登陆完成')
        return self

    @classmethod
    def bulkCreate(cls, accounts):
        clients = []
        for index, account in enumerate(accounts):
            clients.append(cls.create(account, index))
            time.sleep(0.2)
        logger.debug('初始化完成客户端: {}个'.format(len(accounts)))
        return clients

    def forever(self):
        try:
            self.instance.idle()
        except KeyboardInterrupt:
            self.instance.disconnect()
