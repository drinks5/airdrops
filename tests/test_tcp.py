
# encoding: utf-8


from bots.utils import TcpClient

with TcpClient() as client:
    client.recv()
