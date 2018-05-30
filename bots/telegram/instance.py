from apps.accounts import models
from telethon.tl.functions.messages import GetInlineBotResultsRequest
from telethon import TelegramClient, events

from bots.client import Client
from bots.base import BaseDriver as Driver
from apps.contrib import const

client = Client.create(models.Account.objects.get(mobile='17091930610'))


def idle():
    client.instance.idle()
def main():
    while True:
        import time
        time.sleep(0.2)
    pass
