import psycopg
from flask import g
from psycopg.rows import dict_row


def get_db(db_url):
    if 'db' not in g:
        g.db = psycopg.connect(db_url)
        g.db.autocommit = True
    return g.db


def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            return [dict(row) for row in cur]

    def save(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                (url,),
            )
            id = cur.fetchone()[0]
            return id

    def find(self, id):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None