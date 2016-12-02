# -*- coding: utf-8 -*-

import logging

import ujson
from aiohttp import WSMsgType
from aiohttp.web import WebSocketResponse

from .handlers import handlers
from .request import Request, ErrorCode
from .session import Session

log = logging.getLogger(__name__)


async def process_request(data, session, db, sockets, ws):
    log.debug("Request received: %s", data)

    # Try to decode the data. Just stop here if something errors out.
    try:
        message_root = ujson.loads(data.encode('utf-8'))
        message = message_root['data']
    except (UnicodeDecodeError, ValueError, KeyError):
        log.exception("Error while decoding message data")
        return

    # These two may or may not be included
    route = message_root.get('route', None)
    receipt = message_root.get('receipt', None)

    # Handle the request (or at least make an attempt)
    request = Request(message, session, db, sockets, ws, receipt, route)
    try:
        handlers[route](request)
    except KeyError:
        request.send_error({
            'message': 'Server error',
        }, code=ErrorCode.SERVER_ERROR)
        log.exception("Route does not exist!")


async def websocket_handler(request):
    ws = WebSocketResponse()
    await ws.prepare(request)

    request.app['sockets'].add_socket(ws)
    async with request.app['db'].acquire() as db:
        session = Session(db)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await process_request(msg.data, session, db, request.app['sockets'], ws)
            elif msg.type == WSMsgType.ERROR:
                log.error("WS: Socket error: %s", ws.exception())

    request.app['sockets'].del_socket(ws)
    log.info("WS: Connection closed.")
    return ws
