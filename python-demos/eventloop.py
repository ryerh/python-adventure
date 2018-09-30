import select
import sys
import fcntl
import os

from time import time


class EventLoop(object):
    def __init__(self):
        self.stdin_queue = []
        self.timer_queue = []

        self.epoll = select.epoll()
        self.epoll.register(sys.stdin.fileno(), select.EPOLLIN)

        orig_fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

    def process_stdin_on_data(self, callback):
        self.stdin_queue.append(callback)

    def set_interval(self, callback, expire):
        self.timer_queue.append([callback, expire, time()])

    def run_forever(self):
        while True:
            self.dispatch_timer_tasks()
            for fd, evt in self.epoll.poll(timeout=1):
                if fd == sys.stdin.fileno():
                    if evt & select.EPOLLIN:
                        self.dispatch_stdin_tasks()

    def dispatch_stdin_tasks(self):
        line = sys.stdin.read()
        if line.startswith('quit'):
            sys.exit(0)
        for task in self.stdin_queue:
            task(line)

    def dispatch_timer_tasks(self):
        for timer in self.timer_queue:
            task, expire, added = timer
            now = time()
            if now > expire + added:
                timer[2] = now
                task()


def handle_stdin(data):
    print '+ start cpu_task'
    duration = int(data)
    start = time()
    while time() - start < duration:
        pass
    print '+ finish cpu_task'


def handle_timer():
    print '* timer_task'


loop = EventLoop()
loop.process_stdin_on_data(handle_stdin)
loop.set_interval(handle_timer, 3)
loop.run_forever()
