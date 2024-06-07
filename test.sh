#!/bin/bash

source .venv/bin/activate
black *.py
black */*.py
dmypy run -- *.py */*.py
# stop the build if there are Python syntax errors or undefined names
flake8 . --extend-exclude=".venv" --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
flake8 . --extend-exclude=".venv" --ignore=E203,E701,E501,C901,F401,F841 --count --max-line-length=88 --max-complexity=10 --statistics
bandit -r *.py
bandit -r */*.py
pylint --rcfile ./.pylintrc *.py
pylint --rcfile ./.pylintrc */*.py
