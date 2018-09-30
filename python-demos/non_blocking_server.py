# -*- coding: utf8 -*-
#
# Usage:
#   python socket_server.py
#   curl localhost:12345

import select
import socket


class NonBlockingServer(object):
    HOST, PORT = '', 12345
    MAX_QUEUED_CLIS = 5
    CLI_RECV_SIZE = 1024

    def __init__(self):
        self.requests = {}
        self.responses = {}
        self.clients = {}

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(0)
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(self.MAX_QUEUED_CLIS)

        self.e = select.epoll()
        self.e.register(self.s.fileno())

    def serve_forever(self):
        """
        """
        print 'Listing at localhost:{0}'.format(self.PORT)
        try:
            while True:
                for fd, evt in self.e.poll(timeout=1):
                    # PART 1: server fd
                    if fd == self.s.fileno():
                        self.init_client()
                    # PART 2: client fd
                    elif evt & select.EPOLLIN:
                        self.handle_request(fd)
                    elif evt & select.EPOLLOUT:
                        self.handle_response(fd)
        finally:
            self.e.unregister(self.s.fileno())
            self.e.close()
            self.s.close()

    def init_client(self):
        """
        每当有一个新的连接，就把连接的 EPOLLIN 事件加到监听列表里面
        """
        client, addr = self.s.accept()
        print 'Init client connection', addr
        client.setblocking(0)

        fd = client.fileno()
        self.e.register(fd, select.EPOLLIN)
        self.clients[fd] = client
        self.requests[fd] = ''
        self.responses[fd] = ''

    def handle_request(self, fd):
        """
        EPOLLIN 事件触发后，开始读取连接的数据流
        """
        msg = self.recv_msg(fd)
        if msg.find('/q') != -1:
            self.destroy_client(fd)
        else:
            self.send_msg(fd, msg)

    def handle_response(self, fd):
        """
        EPOLLOUT 事件触发后，开始往连接里写入数据流
        """
        msg = self.clients[fd].sendall(self.responses[fd])
        self.responses[fd] = self.responses[fd][msg:]
        self.e.modify(fd, select.EPOLLIN)

    def recv_msg(self, fd):
        msg = self.clients[fd].recv(self.CLI_RECV_SIZE)
        self.requests[fd] += msg
        return msg

    def send_msg(self, fd, msg):
        self.e.modify(fd, select.EPOLLOUT)
        self.responses[fd] = '[{:02d}] ACK\n'.format(fd)
        self.requests[fd] = ''

    def destroy_client(self, fd):
        self.e.unregister(fd)
        self.clients[fd].close()
        del self.clients[fd], self.requests[fd], self.responses[fd]


def main():
    server = NonBlockingServer()
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print ''
        print 'Normally shutting down'
    except Exception as e:
        print ''
        print 'Abnomally shutting down'
        print e.message
