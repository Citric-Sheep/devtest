set -e
echo "🧪 Ejecutando tests en: app/tests"
docker compose exec web bash -c "PYTHONPATH=/DEVTEST pytest app/tests"

