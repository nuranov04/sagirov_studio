#!/bin/sh

until cd /app/

do
    echo "Waiting for db to be ready..."
    sleep 2
done

./manage.py bot
