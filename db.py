import psycopg
from psycopg.rows import dict_row
from config import PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASS

def get_conn():
    conn = psycopg.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASS,
        connect_timeout=5,
        row_factory=dict_row
    )
    with conn.cursor() as cur:
        cur.execute("SET statement_timeout = 3000")  # 3s
        cur.execute("SET default_transaction_read_only = on")
    return conn

def run_select(query: str, params: tuple = ()):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
