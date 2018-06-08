import logging

from django.core.management.base import BaseCommand
from bots.suma.client import start

logger = logging.getLogger('api')


class Command(BaseCommand):

    def handle(self, *args, **options):
        start(args, options)
