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

echo "===== MIGRATE ====="
python manage.py migrate --noinput

echo "===== COLLECTSTATIC ====="
python manage.py collectstatic --noinput

echo "===== SUPERUSER ====="

python manage.py shell <<EOF
print("shell ok")
EOF

echo "===== GUNICORN ====="

exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application