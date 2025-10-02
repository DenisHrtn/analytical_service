#!/bin/sh

echo "Ожидание MongoDB..."
while ! nc -z $MONGO_HOST $MONGO_PORT; do
    sleep 1
done
echo "MongoDB запущена, стартуем FastAPI!"

cd /app/src

exec uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

cd ..