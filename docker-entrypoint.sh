#!/bin/bash
set -e

# Set the PostgreSQL host based on the service name in docker-compose.yaml
DB_HOST="db"
DB_PORT="5432"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL is ready!"


# Run migrations
echo "Running migrations..."
python33 manage.py makemigrations
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Create superuser if env vars provided and no user exists
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
u = User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').first(); \
import sys; \
if not u: User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD'); \
print('superuser created or existed')"
fi

# Create superuser if it doesn't exist (optional)
# Uncomment the following lines if you want to auto-create a superuser
# python3 manage.py shell << EOF
# from accounts.models import User
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'changeme')
# EOF

echo "Starting Gunicorn server..."

exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile - peer_standard_school.wsgi:application