.PHONY: clean-pyc test run

all: clean-pyc test

test:
	py.test tests examples

serve:
	python wsgi.py

work:
	python runworker.py

run:
	python wsgi.py& python runworker.py

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
