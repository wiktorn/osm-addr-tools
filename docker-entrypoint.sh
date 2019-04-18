#!/usr/bin/env sh
set -e

cd /app
venv/bin/gunicorn -t 600 --bind 0.0.0.0:${PORT} wsgi
