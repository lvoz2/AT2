pypy3 -m venv .venv
source .venv/bin/activate
pypy3 -m ensurepip
pypy3 -m pip install --upgrade pip
pypy3 -m pip install flake8 bandit[baseline] pylint
pypy3 -m pip install -U mypy
if [ -f requirements-loc.txt ]; then pypy3 -m pip install --no-index --find-links=wheels/ -r requirements-loc.txt; fi
if [ -f requirements.txt ]; then pypy3 -m pip install -r requirements.txt; fi
