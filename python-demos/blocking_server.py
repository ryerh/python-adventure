#!/usr/bin/env python
#
# Usage:
#   python socket_server.py
#   curl localhost:12345

import socket


class BlockingServer(object):
    HOST, PORT = '', 12345
    MAX_QUEUED_CONNS = 1
    CONN_RECV_SIZE = 1024

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(self.MAX_QUEUED_CONNS)

    def serve_forever(self):
        print 'Listing at localhost:{0}'.format(self.PORT)
        try:
            while True:
                print 'Waiting for connections...'
                conn, addr = self.s.accept()
                try:
                    while True:
                        print 'Waiting for instructions...'
                        msg = conn.recv(self.CONN_RECV_SIZE)
                        if msg.find('/q') != -1:
                            break
                        conn.sendall(msg)
                finally:
                    conn.close()
        finally:
            self.s.close()


def main():
    server = BlockingServer()
    server.serve_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as e:
        print '\nShutting down'
