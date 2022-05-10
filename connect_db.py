import psycopg2


def conn_create():
    conn = psycopg2.connect(
        host="localhost",
        database="ecom",
        user="postgres",
        port="8888",
        password="abc12345")

    cur = conn.cursor()

    return conn, cur
