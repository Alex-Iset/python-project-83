import psycopg2
from flask import g
from psycopg2.extras import RealDictCursor


def get_db(db_url):
    if 'db' not in g:
        g.db = psycopg2.connect(db_url)
        g.db.autocommit = True
    return g.db


def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


class DataBase:
    def __init__(self, conn):
        self.conn = conn

    def save_url(self, url):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                    (url,),
                )
                id = cur.fetchone()[0]
                return id
        except Exception:
            raise

    def find_url(self, id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None
        except Exception:
            raise

    def get_url(self, url):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (url,))
                return cur.fetchone()
        except Exception:
            raise

    def get_urls(self):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls ORDER BY id DESC")
                return [dict(row) for row in cur]
        except Exception:
            raise

    def save_check(self, url_id, status_code, h1, title, description):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description
                    ) VALUES (%s, %s, %s, %s, %s)""",
                    (url_id, status_code, h1, title, description),
                )
        except Exception:
            raise

    def get_checks(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC",
                    (url_id,)
                )
                return [dict(row) for row in cur]
        except Exception:
            raise

    def get_last_check(self, url_id):
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT 
                        created_at, 
                        status_code
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (url_id,)
                )
                return cur.fetchone()
        except Exception:
            raise