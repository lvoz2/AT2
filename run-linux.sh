#!/bin/sh

./install-deps.sh
source .venv/bin/activate
pypy3 game.py
