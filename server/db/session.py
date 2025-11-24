import os
import psycopg2

conn = None
# Get the database URL from the environment variables or the config files
def _get_database_url() -> str:
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        return db_url
    # fall back to config based on APP_ENV like main.py
    env = os.environ.get('APP_ENV', 'development')
    if env == 'production':
        from config_prod import DATABASE_URL  # type: ignore
    else:
        from config_dev import DATABASE_URL  # type: ignore
    return DATABASE_URL


def get_connection():
    db_url = _get_database_url()
    return psycopg2.connect(db_url)

def close_connection_safe(c):
    try:
        if c is not None:
            c.close()
    except Exception:
        pass


# Ping the database to check if it is healthy
def ping() -> bool:
    try:
        c = get_connection()
        try:
            # Open a cursor to perform database operations
            with c.cursor() as cur:
                cur.execute("SELECT 1")
                # Retrieve query results
                _ = cur.fetchone()
            return True
        finally:
            close_connection_safe(c)
    except Exception:
        return False

def create_faq_tables():
    create_faq_sql = """
    CREATE TABLE IF NOT EXISTS posts (
        id SERIAL PRIMARY KEY,
        org_id TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT,
        answer_search TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', answer)) STORED
    );
    """

    try: 
        c = get_connection()
        c.cursor().execute(create_faq_sql)
        c.commit()
    finally:
        close_connection_safe(c)