# -*- coding: utf-8 -*-

import logging
import enum
import ujson

log = logging.getLogger(__name__)


class ErrorCode(enum.Enum):
    SERVER_ERROR = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    VALIDATION_ERROR = 450


class Request(object):
    def __init__(self, message, session, db, sockets, ws, receipt, route):
        self.message = message
        self.session = session
        self.db = db
        self._sockets = sockets
        self._ws = ws
        self.receipt = receipt
        self.route = route

    async def broadcast(self, message, avoid_self=False, route=None):
        data = {'message': message, 'error': False}
        if route or self.route:
            data['route'] = route or self.route
        await self._sockets.broadcast(ujson.dumps(data), avoid_sock=self._ws if avoid_self else None)

    async def send_message(self, message, receipt=None, route=None):
        data = {'message': message, 'error': False}
        if receipt or self.receipt:
            data['receipt'] = receipt or self.receipt
        if route or self.route:
            data['route'] = route or self.route
        await self._ws.send_str(ujson.dumps(data))

    async def send_error(self, error_messages, code, receipt=None, route=None):
        data = {'message': {'error_code': code, 'error_messages': error_messages}, 'error': True}
        if receipt or self.receipt:
            data['receipt'] = receipt or self.receipt
        if route or self.route:
            data['route'] = route or self.route
        await self._ws.send_str(ujson.dumps(data))
