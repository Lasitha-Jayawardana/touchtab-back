#!/usr/bin/env bash
set -e
alembic upgrade head
gunicorn main:app --bind 0.0.0.0:80  --workers 2 --worker-class uvicorn.workers.UvicornWorker --log-level debug
