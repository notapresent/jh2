.PHONY: clean-pyc test run
IP ?= '127.0.0.1'
PORT ?= 8001

all: clean-pyc test

test:
	py.test tests examples

serve:
	gunicorn wsgi:app -c gunicorn_settings.py --bind $(IP):$(PORT)

work:
	rqworker -q -c rqworker_settings

run:
	gunicorn wsgi:app -c gunicorn_settings.py --bind $(IP):$(PORT)& rqworker -q -c rqworker_settings

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

createdb:
	@python -m rbm2m createdb

dropdb:
	@python -m rbm2m dropdb

init:
	@python -m rbm2m dropdb
	@python -m rbm2m createdb
	@python -m rbm2m flush_redis
	@python -m rbm2m import_genres
	@python -m rbm2m reset_settings
