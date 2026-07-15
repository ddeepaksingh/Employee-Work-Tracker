#!/bin/sh

set -ex

echo "===== USER ====="
id

echo "===== ENV ====="
echo "DB_HOST=$DB_HOST"
echo "DB_PORT=$DB_PORT"

echo "===== DIRS ====="
ls -ld /app/staticfiles
ls -ld /app/media
ls -ld /app/logs

echo "===== WAIT DB ====="

until nc -z "$DB_HOST" "$DB_PORT"; do
    sleep 2
done

echo "===== CHOWN MOUNTED VOLUMES ====="
chown -R appuser:appgroup /app/media /app/staticfiles /app/logs

echo "===== MIGRATE ====="
su-exec appuser python manage.py migrate --noinput

echo "===== COLLECTSTATIC ====="
su-exec appuser python manage.py collectstatic --noinput

echo "===== SUPERUSER ====="

su-exec appuser python manage.py shell <<EOF
print("shell ok")
EOF

echo "===== GUNICORN ====="

exec su-exec appuser gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class gthread \
    --threads 4 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application