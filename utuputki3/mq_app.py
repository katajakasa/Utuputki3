# -*- coding: utf-8 -*-

import logging
from uuid import uuid1

import asyncio

from .init_helpers import init_db, init_mq, close_db, close_mq
from .mq_handlers import message_handler

log = logging.getLogger(__name__)


class Application(object):
    def __init__(self, loop):
        self.on_startup = []
        self.on_cleanup = []
        self._state = {}
        self.loop = loop

    async def run_startup_cbs(self):
        for fn in self.on_startup:
            await fn(self)

    async def run_cleanup_cbs(self):
        for fn in self.on_cleanup:
            await fn(self)

    def __getitem__(self, key):
        return self._state[key]

    def __setitem__(self, key, value):
        self._state[key] = value

    def __delitem__(self, key):
        del self._state[key]

    def __len__(self):
        return len(self._state)

    def __iter__(self):
        return iter(self._state)


def run_app(config):
    loop = asyncio.get_event_loop()

    app = Application(loop=loop)
    app['config'] = config

    # Startup and shutdown callbacks
    for fn in [init_db, init_mq]:
        app.on_startup.append(fn)
    for fn in [close_db, close_mq]:
        app.on_cleanup.append(fn)

    # Run startup jobs
    loop.run_until_complete(app.run_startup_cbs())

    # Get an MQ connection/channel from the pool
    mq_connection = app['mq'].acquire()

    # Callback for received messages. This is a dummy, it just calls the
    async def on_request(channel, body, envelope, properties):
        await message_handler(app, mq_connection, body, envelope.delivery_tag)

    # Setup listener
    consumer_tag = str(uuid1())
    loop.run_until_complete(mq_connection.consume(on_request, consumer_tag))

    # Run listener until cancelled
    print("======= Running on amqp://{} ======".format(config['mq-link']['queue-in']))
    print("(Press CTRL+C to quit)")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(mq_connection.cancel(consumer_tag))
        mq_connection.release()
        loop.run_until_complete(app.run_cleanup_cbs())
    loop.close()
