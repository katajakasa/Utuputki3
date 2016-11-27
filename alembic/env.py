from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import dictConfig

import sys
sys.path.append("..")
sys.path.append(".")

from utuputki3.config import read_config
from utuputki3 import db

app_config = read_config()  # Config from the json file
config = context.config  # Config from the ini file
dictConfig(app_config['logging'])
target_metadata = db.metadata
config.set_main_option(
    'sqlalchemy.url',
    'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        app_config['database']['username'],
        app_config['database']['password'],
        app_config['database']['host'],
        app_config['database']['port'],
        app_config['database']['database']))


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            compare_type=True,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
