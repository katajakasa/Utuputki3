# -*- coding: utf-8 -*-

import logging

from asyncpg import create_pool

from .sockhandler import SockHandler

log = logging.getLogger(__name__)


async def init_db(app):
    conf = app['config']['database']
    engine = await create_pool(
        database=conf['database'],
        user=conf['username'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        min_size=conf['minsize'],
        max_size=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine
    log.info("DB: Connected")

async def init_sockets(app):
    app['sockets'] = SockHandler()

async def close_sockets(app):
    app['sockets'].close()

async def close_db(app):
    await app['db'].close()
    log.info("DB: Connection closed")
