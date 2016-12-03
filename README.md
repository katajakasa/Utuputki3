# Utuputki3

Asynchronous lanparty video playlist management and video streaming application.

## Requirements

Python 3.5 and PostgreSQL

## Installation

1. Create a virtualenv for python 3.5 and activate it
2. Create a database table and user (with password)
3. Copy utuputki3.json.dist to utuputki3.json and modify (add database info)
4. Install python libraries: `pip install -r requirements.txt`
5. Run migrations: `alembic upgrade head`
6. Run! (see below)

## Startup

### 1. Production, fastest solution

This only works on linux, and you need to have the uvloop python package installed.
Easily the fastest solution. To install the missing package, run `pip install uvloop`.

`gunicorn utuputki3.gu_app:app --worker-class aiohttp.worker.GunicornUVLoopWebWorker --bind localhost:8080`

### 2. Production, without uvloop

Second best solution, again only works on linux.

`gunicorn utuputki3.gu_app:app --worker-class aiohttp.worker.GunicornWebWorker --bind localhost:8080`

### 3. Testing or for windows

Only use this if you don't have have another solution or are testing/developing

`python -m aiohttp.web -H localhost -P 8080 utuputki3.app:get_app`

## License

MIT. See `LICENSE` file for details.
