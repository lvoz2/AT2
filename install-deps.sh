pypy -m venv .venv
source .venv/bin/activate
pypy -m ensurepip
pypy -m pip install --upgrade pip
pypy -m pip install flake8 bandit[baseline] pylint
pypy -m pip install -U mypy
git clone https://github.com/pygame/pygame.git
cd pygame
pypy3 setup.py -config -auto
pypy3 setup.py build
pypy3 setup.py install --user
cd ..
if [ -f requirements.txt ]; then pypy -m pip install -r requirements.txt; fi
