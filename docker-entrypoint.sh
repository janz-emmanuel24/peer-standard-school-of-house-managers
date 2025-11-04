#!/bin/bash
set -e

# Only wait for PostgreSQL if we're using it
if [ "${DB_ENGINE:-sqlite3}" = "postgresql" ]; then
    echo "Waiting for PostgreSQL to be ready..."
    until nc -z $DB_HOST ${DB_PORT:-5432}; do
      echo "Waiting for PostgreSQL..."
      sleep 1
    done
    echo "PostgreSQL is ready!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
# Uncomment the following lines if you want to auto-create a superuser
# python manage.py shell << EOF
# from accounts.models import User
# if not User.objects.filter(is_superuser=True).exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'changeme')
# EOF

echo "Starting server..."
exec "$@"

