.PHONY: clean-pyc test run

all: clean-pyc test

test:
	# TODO use actual command
	py.test tests examples

serve:
	python wsgi.py

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
