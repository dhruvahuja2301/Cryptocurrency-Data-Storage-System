from env import database, host, user, password
import psycopg2

def mydbfunc():
    try:
        return psycopg2.connect(host=host, user=user, password=password, database=database)
    except Exception as e:
        return e
