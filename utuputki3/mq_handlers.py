# -*- coding: utf-8 -*-

import logging
import ujson

from .db import test_table

log = logging.getLogger(__name__)


async def message_handler(app, listener, body, delivery_tag):
    try:
        message = ujson.loads(body.decode('utf-8'))
    except (UnicodeDecodeError, ValueError):
        await listener.nack(delivery_tag)
        log.exception("NACK delivery_tag=%s: Could not decode message", delivery_tag, extra={'body': body})
        return

    db_engine = app['db']
    mq_engine = app['mq']
    async with db_engine.acquire() as db_connection, mq_engine.acquire() as mq_connection:
        try:
            await db_connection.execute(test_table.insert().values(value=message['uuid']))
            await listener.ack(delivery_tag)
            log.info("ACK delivery_tag=%s", delivery_tag)
        except:
            await listener.nack(delivery_tag)
            log.exception("NACK delivery_tag=%s: Handler exception", delivery_tag, extra={'body': body})
