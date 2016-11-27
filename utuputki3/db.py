# -*- coding: utf-8 -*-

import arrow
import sqlalchemy as sa

metadata = sa.MetaData()


def utc_now():
    return arrow.utcnow().datetime


user_table = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Integer),
    sa.Column('username', sa.Unicode(32), unique=True, nullable=False),
    sa.Column('password', sa.Unicode(32), nullable=False),
    sa.Column('nickname', sa.Unicode(32), nullable=False),
    sa.Column('email', sa.Unicode(128), nullable=False),
    sa.Column('level', sa.Integer, default=0, nullable=False),
    sa.Column('created_at', sa.DateTime, default=utc_now, nullable=False),
    sa.Column('updated_at', sa.DateTime, default=utc_now, onupdate=utc_now, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_id_pkey'),
)

test_table = sa.Table(
    'test',
    metadata,
    sa.Column('id', sa.Integer),
    sa.Column('value', sa.Unicode(36), nullable=False),
    sa.PrimaryKeyConstraint('id', name='test_id_pkey'),
)
