# -*- coding: utf-8 -*-

import logging
import queue
import ujson

log = logging.getLogger(__name__)


class MQEngine(object):
    def __init__(self, transport, protocol, config):
        self.transport = transport
        self.protocol = protocol
        self.exchange = config['mq-link']['exchange']
        self.queue_in = config['mq-link']['queue-in']
        self.queue_out = config['mq-link']['queue-out']
        self.min_pool_size = config['amqp']['minsize']
        self.max_pool_size = config['amqp']['maxsize']
        self._pool = queue.Queue(maxsize=self.max_pool_size)

    async def prepare_pool(self):
        for m in range(0, self.min_pool_size):
            obj = self._create()
            await obj.connect()
            self._pool.put_nowait(obj)

    def acquire(self):
        try:
            obj = self._pool.get(False)
        except queue.Empty:
            obj = self._create()
        return obj

    def release(self, obj):
        try:
            self._pool.put_nowait(obj)
        except queue.Full:
            obj.channel.close()

    def _create(self):
        return MQConnection(
            engine=self,
            protocol=self.protocol,
            exchange=self.exchange,
            queue_in=self.queue_in,
            queue_out=self.queue_out)

    async def close(self):
        await self.protocol.close()
        self.transport.close()


class MQConnection(object):
    def __init__(self, engine, protocol, exchange, queue_in, queue_out):
        self.engine = engine
        self.protocol = protocol
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.queue_in_obj = None
        self.queue_out_obj = None
        self.exchange = exchange
        self.channel = None

    async def consume(self, callback, consumer_tag):
        await self.channel.basic_consume(callback, consumer_tag=consumer_tag, queue_name=self.queue_out)

    async def cancel(self, consumer_tag):
        await self.channel.basic_cancel(consumer_tag=consumer_tag)

    async def publish(self, message, correlation_id):
        await self.channel.basic_publish(
            payload=ujson.dumps(message, ensure_ascii=False).encode('utf-8'),
            exchange_name=self.exchange,
            routing_key=self.queue_out,
            mandatory=True,
            properties={
                'content_type': 'application/json',
                'delivery_mode': 2,
                'correlation_id': correlation_id
            })

    async def ack(self, delivery_tag):
        await self.channel.basic_client_ack(delivery_tag=delivery_tag)

    async def nack(self, delivery_tag):
        await self.channel.basic_client_nack(delivery_tag=delivery_tag)

    async def connect(self):
        if not self.channel:
            self.channel = await self.protocol.channel()
            await self.channel.exchange(
                exchange_name=self.exchange,
                type_name='direct',
                durable=True,
                auto_delete=False)
            self.queue_in_obj = await self.channel.queue(
                queue_name=self.queue_in,
                durable=True,
                auto_delete=False)
            self.queue_out_obj = await self.channel.queue(
                queue_name=self.queue_out,
                durable=True,
                auto_delete=False)
            await self.channel.queue_bind(
                exchange_name=self.exchange,
                queue_name=self.queue_in,
                routing_key=self.queue_in)
            await self.channel.queue_bind(
                exchange_name=self.exchange,
                queue_name=self.queue_out,
                routing_key=self.queue_out)

    async def __aenter__(self):
        await self.connect()
        return self

    def release(self):
        self.engine.release(self)

    async def __aexit__(self, exc_type, exc, tb):
        self.engine.release(self)

    def __await__(self):
        return self.__aenter__().__await__()
