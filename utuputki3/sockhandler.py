# -*- coding: utf-8 -*-

import asyncio


class SockHandler(object):
    def __init__(self):
        self.sockets = set()

    def broadcast(self, message, avoid_sock=None):
        for socket in self.sockets:
            if avoid_sock and avoid_sock == socket:
                continue
            socket.send_str(message)

    def add_socket(self, ws):
        self.sockets.add(ws)

    def del_socket(self, ws):
        self.sockets.remove(ws)
