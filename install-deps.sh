python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flake8 bandit[baseline]
python -m pip install -U mypy
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
