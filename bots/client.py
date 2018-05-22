# encoding: utf-8

import logging

import telethon
from telethon import TelegramClient, events
import socks
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from faker import Faker

from apps.contrib import const
from .utils import logError, Command, sleep

logger = logging.getLogger('api')


class Dispatch(object):
    client = None

    def __init__(self, client):
        self.client = client

    def joinMyChannel(self):
        try:
            self.client.instance(ImportChatInviteRequest(const.MyChannel))
        except telethon.errors.rpc_error_list.UserAlreadyParticipantError:
            pass
        except Exception:
            logError()

    def joinChannel(self, command):
        logger.debug('start command joinChannel {}'.format(command))
        groupLink = command.para[0]
        try:
            group = self.client.instance.get_entity(groupLink)
            self.client.instance(JoinChannelRequest(group))
            logger.debug('finish command joinChannel')
        except Exception:
            logError()

    def sendMessage(self, command):
        self.client.instance.send_message(
            command.para[0],
            command.para[1].format(name=self.client.account.name))

    def updateUsername(self, command):
        while True:
            import time
            faker = Faker()
            username = faker.name()
            username = ''.join(username.split(' '))
            try:
                logger.debug('updateUsername {}'.format(username))
                self.client.instance(UpdateUsernameRequest(username))
                self.client.account.name = username
                self.client.account.save()
                logger.debug('finish updateUsername {}'.format(username))
                return
            except:
                logError()
            time.sleep(1)

    def excute(self, command):
        method = getattr(self, command.name, None)
        if not method:
            return
        return method(command)


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
            proxy=(socks.SOCKS5, '127.0.0.1', 1080),
            update_workers=4,
            spawn_read_thread=False)
        self.dispatch = Dispatch(self)

    def OnMessage(self, event):
        command = Command(event.raw_text)
        if command.mobile and command.mobile != self.account.mobile:
            return
        try:
            self.dispatch.excute(command)
        except Exception:
            logError()

    @classmethod
    def create(cls, account):
        self = cls(account)
        self.instance.start()
        self.instance.on(events.NewMessage)(self.OnMessage)
        self.dispatch.joinMyChannel()
        logger.debug('finished me: {}'.format(self.instance.get_me()))
        return self

    @classmethod
    def bulkCreate(cls, accounts):
        clients = [Client.create(account) for account in accounts[:]]
        logger.debug('初始化完成客户端: {}个'.format(len(accounts)))
        return clients

    def forever(self):
        try:
            self.instance.idle()
        except KeyboardInterrupt:
            self.instance.disconnect()
