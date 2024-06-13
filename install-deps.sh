if [ ! -d ./.venv ]; then
    pypy -m venv .venv
fi
source .venv/bin/activate
pypy3 -m ensurepip
pypy3 -m pip install --upgrade pip
pypy3 -m pip install flake8 bandit[baseline] pylint black
pypy3 -m pip install -U mypy
if [ -f requirements.txt ]; then pypy3 -m pip install -r requirements.txt; fi
