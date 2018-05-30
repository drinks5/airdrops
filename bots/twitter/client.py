import twitter

proxies={'http':'http://127.0.0.1:1087',
         'https':'https://127.0.0.1:1087'}

class Client(object):
    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token_key,
                 access_token_secret,
                 mobile='10086'):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.mobile = mobile
        self.verify()

    def verify(self):
        self.api = twitter.Api(consumer_key=self.consumer_key,
                               consumer_secret=self.consumer_secret,
                               access_token_key=self.access_token_key,
                               access_token_secret=self.access_token_secret,
                               proxies=proxies)
        user = self.api.VerifyCredentials()
        self.id = user.id
        self.screen_name = user.screen_name

    def send_message(self, message):
        status = self.api.PostUpdate(message)
        return True if status.text == message else False

    def like(self, id=None, screen_name=None, follow=True):
        if id:
            self.api.CreateFriendship(user_id=id, follow=follow)
        if screen_name:
            self.api.CreateFriendship(screen_name=screen_name, follow=follow)

    def dislike(self, id=None, screen_name=None):
        self.like(self, id, screen_name, False)

    def get_friend_IDs(self):
        return self.api.GetFriendIDs()


def get_clients():
    clients = list()
    clients.append(Client(access_token_key='985070023654834176-fQybS5THVgNdd0cQBESgXooQM2ACHBF',
                           access_token_secret='5TeHOVpaiblc7kltVeJd7IqLJYexwLr9DGxMi96kdy6fi',
                           consumer_key='aB0MaDinqWWI6oK66HSP3qNUc',
                           consumer_secret = 'VJY70cfxb8ifpog8GeOWCfrODuzrpVNR9hMgFc3i18NAzIMwPW'))
    return clients

