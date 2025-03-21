#!/bin/sh

cd /app/src

PYTHONPATH=uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload