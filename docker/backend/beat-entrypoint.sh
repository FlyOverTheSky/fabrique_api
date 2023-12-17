#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run a beat :)
celery -A backend beat --loglevel=info
