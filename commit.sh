#!/bin/bash

env/bin/python -m bandit -r ./src/ -lll -iii
env/bin/python -m pytest ./src

env/bin/python -m ruff check ./src --fix
env/bin/python -m ruff check server.py --fix

env/bin/python -m black ./src; env/bin/python -m isort ./src
env/bin/python -m black server.py; env/bin/python -m isort server.py