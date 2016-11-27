# -*- coding: utf-8 -*-

import logging


import asyncio
from aiohttp import web
import aioamqp
import pymysql

from .web_handlers import index
from .init_helpers import init_db, init_mq, close_db, close_mq

log = logging.getLogger(__name__)


def run_app(config):
    loop = asyncio.get_event_loop()
    app = web.Application(
        loop=loop,
        debug=config['debug'])
    app['config'] = config

    # Startup and shutdown callbacks
    for fn in [init_db, init_mq]:
        app.on_startup.append(fn)
    for fn in [close_db, close_mq]:
        app.on_cleanup.append(fn)

    # Routes
    app.router.add_get('/', index)

    # Run web server until shutdown signal is received. Handles init and close callbacks.
    # Init functions may throw exceptions, catch those.
    web_conf = config['web']
    try:
        web.run_app(
            app=app,
            host=web_conf['host'],
            port=web_conf['port'])
    except pymysql.err.OperationalError:
        db_conf = config['database']
        log.exception("Unable to connect to database %s@%s:%s",
                      db_conf['database'], db_conf['host'], db_conf['port'])
        exit(1)
    except aioamqp.exceptions.AmqpClosedConnection:
        mq_conf = config['amqp']
        log.exception("Unable to connect to amqp server %s@%s:%s",
                      mq_conf['virtualhost'], mq_conf['host'], mq_conf['port'])
        exit(1)

    exit(0)
