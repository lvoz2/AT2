#!/bin/bash

source .venv/bin/activate
dmypy run -- *.py
dmypy run -- */*.py
# stop the build if there are Python syntax errors or undefined names
flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 */*.py --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
flake8 *.py --ignore=C901 --count --exit-zero --max-complexity=10 --max-line-length=319 --statistics
flake8 */*.py --count --exit-zero --max-complexity=10 --max-line-length=319 --statistics
bandit -r *.py
bandit -r */*.py
pylint --rcfile ./.pylintrc *.py
pylint --rcfile ./.pylintrc */*.py
