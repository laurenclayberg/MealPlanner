import psycopg2
import os

def singleton(fn):
    value_set = False
    value = None
    def wrapped():
        nonlocal value_set, value
        if not value_set:
            value = fn()
            value_set = True
        return value
    return wrapped

@singleton
def db():
    return psycopg2.connect(
        dbname=os.environ.get("PSQL_DB", "postgres"),
        user=os.environ.get("PSQL_USER", "postgres"),
        host=os.environ.get("PSQL_HOST", "localhost"),
        port=int(os.environ.get("PSQL_PORT", "5432")),
        password=os.environ.get("PSQL_PASS", ""),
    )
