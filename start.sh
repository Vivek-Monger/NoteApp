#!/bin/bash
# Django NoteApp Startup Script
# This script runs database migrations and starts the Django development server

set -e

echo "=== Django NoteApp Starting ==="
echo ""
echo "Creating data directory if needed..."
mkdir -p data

echo "Running database migrations..."
python manage.py migrate --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || true

echo ""
echo "Starting Django development server on 0.0.0.0:8000..."
echo "Visit: http://localhost:8000"
echo ""
python manage.py runserver 0.0.0.0:8000

