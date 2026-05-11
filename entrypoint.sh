#!/bin/sh

set -e

DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

INIT_FLAG="/django_initialized"

echo "Aguardando banco de dados em ${DB_HOST}:${DB_PORT}..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "Banco de dados disponível."

if [ ! -f "$INIT_FLAG" ]; then
  echo "Executando migrations..."
  python manage.py collectstatic  --noinput
  python manage.py makemigrations --noinput
  python manage.py migrate --noinput
  python manage.py loaddata core/fixtures/form_fields.json core/fixtures/index_map.json

  touch "$INIT_FLAG"

  echo "Inicialização concluída."
else
  echo "Migrations já executadas anteriormente."
fi

echo "Iniciando aplicação..."

exec "$@"
