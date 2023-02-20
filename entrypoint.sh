#! /usr/bin/env bash

if [ "$1" = "cron" ]; then
  echo "Migrating backend..."
  cd balanced_backend
  alembic upgrade head
  echo "Starting cron..."
  python main_cron.py
elif [ "$1" = "streaming" ]; then
  echo "Starting stream processor..."
  python balanced_backend/main_streaming.py
elif [ "$1" = "api" ]; then
  echo "Starting API..."
  python balanced_backend/main_api.py
else
  echo "No args specified - exiting..."
fi
