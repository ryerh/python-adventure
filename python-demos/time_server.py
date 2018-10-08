# coding: utf8

import socket
import sys
import time

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8888))
    s.listen(5)

    while True:
        c, addr = s.accept()
        t = time.ctime(time.time()) + '\r\n'
        c.send(t)
        c.close()

if __name__ == '__main__':
    try:
        main()
    except:
        sys.exit(0)
