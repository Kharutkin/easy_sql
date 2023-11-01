import psycopg2
from config import host, user, password, db_name


def req_to_db(req):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(req)
            return cursor.fetchall()

    except Exception as _ex:
        print('[INFO] Error while working PostgreSQL', _ex)

    finally:
        if connection:
            # cursor.close()
            connection.close()
            print('[INFO] Error while working PostgreSQL closed')
