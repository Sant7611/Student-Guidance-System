#!/bin/sh

set -e

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Loading seed data..."
python manage.py seed_data

echo "Starting Django server..."
exec daphne -b 0.0.0.0 -p ${PORT:-9009} student_guidance_system.asgi:application