#!/bin/bash

source .venv/bin/activate
dmypy run -- *.py
dmypy run -- */*.py
# stop the build if there are Python syntax errors or undefined names
flake8 . --exclude ['.venv', '.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox', '.eggs', '*.egg'] --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings
flake8 . --exclude ['.venv', '.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox', '.eggs', '*.egg'] --ignore=C901 --count --exit-zero --max-complexity=10 --max-line-length=319 --statistics
bandit -r *.py
bandit -r */*.py
pylint --rcfile ./.pylintrc .
