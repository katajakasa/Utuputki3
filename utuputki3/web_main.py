# -*- coding: utf-8 -*-

import argparse
from logging.config import dictConfig

from .web_app import run_app
from .config import read_config

try:
    import uvloop
    import asyncio
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


def main():
    parser = argparse.ArgumentParser(description='Utuputki3 server application')
    parser.add_argument('--config', type=str, default=None, help='Config file')
    args = parser.parse_args()
    override_file = args.config

    # Read the config file
    config = read_config(override_file)
    if not config:
        print("Configuration file not found!")
        exit(1)

    # Set up logging
    dictConfig(config['logging'])

    # Run application! Whee!
    run_app(config)


if __name__ == "__main__":
    main()
