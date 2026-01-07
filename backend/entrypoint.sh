#!/bin/sh

set -e

echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo "Creating superuser (hardcoded, if not exists)..."

# Create superuser non-interactively (will fail if exists, so we ignore)
python manage.py createsuperuser \
  --username admin \
  --email admin@example.com \
  --noinput || true

python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.get(username="admin")
user.set_password("admin123")
user.is_staff = True
user.is_superuser = True
user.save()
EOF

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4