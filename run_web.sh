#!/bin/bash

gunicorn utuputki3:web_main --bind localhost:8080 --workers=2 --worker-class aiohttp.worker.GunicornUVLoopWebWorker