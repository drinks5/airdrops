import time
import logging

from flanker import mime
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from django.conf import settings

from apps.accounts.models import Link

logger = logging.getLogger('api')


def getHrefs(eml):
    msg = mime.from_string(eml)
    if not msg.parts or not len(msg.parts) > 1:
        return []
    links = BeautifulSoup(msg.parts[1].body, 'html.parser').find_all('a')
    hrefs = [(x.get('href'), x.text) for x in links]
    return hrefs


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if not event.is_directory:
            print("file created:{0}".format(event.src_path))
            try:
                with open(event.src_path, 'r') as fd:
                    hrefs = getHrefs(fd.read())
            except FileNotFoundError:
                return
            for text, href in hrefs:
                try:
                    Link.objects.get_or_create(href=href, text=text)
                    logger.info('create {}'.format(href))
                except Exception as e:
                    logger.error(e)


def watchDog():
    path = str(settings.ROOT_DIR.path('maildata'))
    print('开始监听目录:{}'.format(path))
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,  path, True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watchDog()
