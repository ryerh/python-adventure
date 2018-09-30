import logging
import sys
import socket
import select

_MAX_CONNECTION_BACKLOG = 1
_PORT = 9999
_BINDING = ('0.0.0.0', _PORT)
_EPOLL_BLOCK_DURATION_S = 1

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

_CONNECTIONS = {}

_EVENT_LOOKUP = {
    select.POLLIN: 'POLLIN',
    select.POLLPRI: 'POLLPRI',
    select.POLLOUT: 'POLLOUT',
    select.POLLERR: 'POLLERR',
    select.POLLHUP: 'POLLHUP',
    select.POLLNVAL: 'POLLNVAL',
}

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)

def _get_flag_names(flags):
    names = []
    for bit, name in _EVENT_LOOKUP.items():
        if flags & bit:
            names.append(name)
            flags -= bit

            if flags == 0:
                break

    assert flags == 0, "We couldn't account for all flags: (%d)" % (flags,)

    return names

def _handle_inotify_event(epoll, server, fd, event_type):
    # Common, but we're not interested.
    if (event_type & select.POLLOUT) == 0:
        flag_list = _get_flag_names(event_type)
        _LOGGER.debug("Received (%d): %s",
                      fd, flag_list)

    # Activity on the master socket means a new connection.
    if fd == server.fileno():
        _LOGGER.debug("Received connection: (%d)", event_type)

        c, address = server.accept()
        c.setblocking(0)

        child_fd = c.fileno()

        # Start watching the new connection.
        epoll.register(child_fd)

        _CONNECTIONS[child_fd] = c
    else:
        c = _CONNECTIONS[fd]

        # Child connection can read.
        if event_type & select.EPOLLIN:
            b = c.recv(1024)
            sys.stdout.write(b)

def _create_server_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(_BINDING)
    s.listen(_MAX_CONNECTION_BACKLOG)
    s.setblocking(0)

    return s

def _run_server():
    s = _create_server_socket()

    e = select.epoll()

    # If not provided, event-mask defaults to (POLLIN | POLLPRI | POLLOUT). It
    # can be modified later with modify().
    e.register(s.fileno())

    try:
        while True:
            events = e.poll(_EPOLL_BLOCK_DURATION_S)
            for fd, event_type in events:
                _handle_inotify_event(e, s, fd, event_type)
    finally:
        e.unregister(s.fileno())
        e.close()
        s.close()

if __name__ == '__main__':
    _configure_logging()
    _run_server()
