import sys
from client import get_clients

def test(*args):
    print(test)
    print(args)

def like(*args):
    if len(args) == 0:
        return

    def func(client):
        client.like(screen_name=args[0])

    invoke(func,args)


def send(*args):
    if len(args) == 0:
        return
    message = args[0]

    def func(client):
        client.send_message(message)

    invoke(func, args)


def invoke(func, args):
    clients = get_clients()
    if len(args) == 1:
        for client in clients:
            func(client)
    else:
        for arg in args[1:]:
            if arg[0] != '-':
                continue
            equal = arg.find('=')
            key = arg[1:equal]
            value = arg[equal + 1:]
            for client in clients:
                if getattr(client, key) == value:
                    func(client)

def main():
    argv = sys.argv
    if len(argv) < 2:
        pass
    else:
        action = argv[1]
        globals()[action](*argv[2:])



if __name__ == '__main__':
    main()

