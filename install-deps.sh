pypy -m venv .venv
source .venv/bin/activate
pypy -m pip install --upgrade pip
pypy -m pip install flake8 bandit[baseline]
pypy -m pip install -U mypy
if [ -f requirements.txt ]; then pypy -m pip install -r requirements.txt; fi
