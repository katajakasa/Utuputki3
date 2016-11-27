# -*- coding: utf-8 -*-

import logging
from uuid import uuid1

from aiohttp.web import Response
from .db import test_table

log = logging.getLogger(__name__)


async def index(request):
    db_engine = request.app['db']
    mq_engine = request.app['mq']
    async with db_engine.acquire() as db_connection, mq_engine.acquire() as mq_connection:
        # Attempt to run the handler
        try:
            m_uuid = str(uuid1())
            await db_connection.execute(test_table.insert().values(value=m_uuid))
            # await mq_connection.publish({'uuid': m_uuid}, correlation_id=m_uuid)
        except Exception as e:
            log.exception("Error while running handler", exc_info=e)

    return Response(text='OK')
