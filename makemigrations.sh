set -e

MSG=$1

if [ -z "$MSG" ]; then
  echo "❌ Pass a migration message as an argument:"
  echo "./makemigrations.sh \"mensaje de migración\""
  exit 1
fi

echo "Generating migration with Alembic in the container..."

docker compose exec web alembic revision --autogenerate -m "$MSG"

echo "Applying migration to DB..."
docker compose exec web alembic upgrade head

echo "Migration Created!!"

