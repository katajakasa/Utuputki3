# -*- coding: utf-8 -*-

import logging
import socket

import asyncio
from aiohttp import web
from aiomysql.sa import create_engine
import aioamqp
from aioamqp import connect as amqp_connect
import pymysql

from .handlers import index
from .mq_connection import MQEngine

log = logging.getLogger(__name__)


async def init_db(app):
    conf = app['config']['database']
    engine = await create_engine(
        db=conf['database'],
        user=conf['username'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        autocommit=True,
        loop=app.loop)
    app['db'] = engine
    log.info("DB: Connected")

async def init_mq(app):
    conf = app['config']['amqp']
    transport, protocol = await amqp_connect(
        host=conf['host'],
        port=conf['port'],
        login=conf['username'],
        password=conf['password'],
        virtualhost=conf['virtualhost'],
        ssl=conf['ssl'],
        verify_ssl=conf['verify_ssl'],
        heartbeat=conf['heartbeat'],
        insist=True,
        loop=app.loop,
        client_properties={
            'program_name': "Utuputki3",
            'hostname': socket.gethostname(),
        },
    )
    app['mq'] = MQEngine(transport, protocol, app['config'])
    await app['mq'].prepare_pool()
    log.info("MQ: Connected")

async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()
    log.info("DB: Connection closed")

async def close_mq(app):
    await app['mq'].close()
    log.info("MQ: Connection closed")


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
