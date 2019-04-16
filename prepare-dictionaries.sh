#!/usr/bin/env sh
set -e

cd /app
venv/bin/python prepare-dictionaries.py
