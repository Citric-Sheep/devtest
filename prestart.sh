# prestart.sh

echo "Waiting for DB connection"

while ! ncat -z db 3307; do
    sleep 0.1
done

echo "DB started"

exec "$@"
