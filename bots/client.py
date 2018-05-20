# encoding: utf-8

import logging
import random

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
        logger.debug('start command joinChannel')
        groupLink = command.para
        try:
            group = self.client.instance.get_entity(groupLink)
            self.client.instance(JoinChannelRequest(group))
            logger.debug('finish command joinChannel')
        except Exception:
            logError()

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

        # username = command.para or self.client.account.name
        # username = ''.join(username.split(' '))
        # self.client.instance(UpdateUsernameRequest(username))

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
        try:
            command = Command(event.raw_text)
            self.dispatch.excute(command)
        except Exception:
            logError()

    def forever(self, *args):
        self.instance.start()
        self.instance.on(events.NewMessage)(self.OnMessage)
        logger.debug('finished me: {}'.format(self.instance.get_me()))
        try:
            self.instance.idle()
        except KeyboardInterrupt:
            self.instance.disconnect()
