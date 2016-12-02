# -*- coding: utf-8 -*-

import logging
from logging.config import dictConfig

import asyncio
from aiohttp import web

from .web_handlers import websocket_handler
from .init_helpers import init_db, init_sockets, close_db, close_sockets
from .config import read_config

log = logging.getLogger(__name__)


def get_app(argv=None):
    # Read the config file
    config = read_config()

    # Set up logging
    dictConfig(config['logging'])
    log = logging.getLogger(__name__)

    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop, debug=config['debug'])
    app['config'] = config

    # Startup and shutdown callbacks
    for fn in [init_db, init_sockets]:
        app.on_startup.append(fn)
    for fn in [close_db, close_sockets]:
        app.on_cleanup.append(fn)

    # Routes
    app.router.add_get('/ws', websocket_handler)
    return app
