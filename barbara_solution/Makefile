SHELL := /bin/bash

lint:		## Run lint checks
	flake8 .
	black . --line-length 79 --check

test: lint	## Run lint checks and unit tests
	pytest tests

format:		## Format code according to lint checks
	black --line-length 79 .

install:	## Install dependencies
	pip install -r requirements.txt

run: 	## Run app
	PYTHONPATH=$(shell pwd) python main.py