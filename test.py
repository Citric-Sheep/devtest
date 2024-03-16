import psycopg2
from psycopg2 import OperationalError

def test_postgresql_connection():
    try:
        # Parámetros de conexión a PostgreSQL
        dbname = 'elevator'
        user = 'postgres'
        password = 'password'
        host = 'localhost'
        port = 5432

        # Intenta establecer una conexión a PostgreSQL
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

        # Si la conexión se realiza correctamente, imprime un mensaje
        print("La conexión a PostgreSQL fue exitosa.")

        # Cierra la conexión
        conn.close()

    except OperationalError as e:
        # Si hay un error al intentar conectarse, imprime el mensaje de error
        print("Error al conectarse a PostgreSQL:", e)

if __name__ == "__main__":
    test_postgresql_connection()
