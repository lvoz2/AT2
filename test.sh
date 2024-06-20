#!/bin/bash

source .venv/bin/activate
black **/*.py
isort --profile black **/*.py
dmypy run -- **/*.py
# stop the build if there are Python syntax errors or undefined names
flake8 **/*.py --extend-exclude=".venv" --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
flake8 **/*.py --extend-exclude=".venv" --ignore=E203,E701,E501,C901,F401,F841,W503 --count --max-line-length=88 --max-complexity=10 --statistics
bandit -r **/*.py
pylint --rcfile ./.pylintrc **/*.py