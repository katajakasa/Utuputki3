# -*- coding: utf-8 -*-

import socket
import logging

from aiomysql.sa import create_engine
from aioamqp import connect as amqp_connect

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
