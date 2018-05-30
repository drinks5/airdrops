import sys
from .client import get_clients


def like(*args):
    """
    ./twitter link xxxx
    """
    if len(args) == 0:
        return
    # 构建回调函数
    def func(client):
        client.like(screen_name=args[0])
    invoke(func, args)


def send(*args):
    """
    ./twitter send xxxx
    """
    if len(args) == 0:
        return
    message = args[0]
    def func(client):
        client.send_message(message)
    invoke(func, args)


def invoke(func, args):
    clients = get_clients()
    if len(args) == 1:
    # 只有一个参数，对所有client都回调函数
        for client in clients:
            func(client)
    else:
    # 寻找-{attr}={value} 的参数，对符合条件的client调用
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
    """
	命令行参数，调用名为argv[1]的函数，其他argvs作为参数传入
    """
    argv = sys.argv
    if len(argv) < 2:
        pass
    else:
        globals()[argv[1](*argv[2:])


if __name__ == '__main__':
    main()
