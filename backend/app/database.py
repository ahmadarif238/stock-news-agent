"""Database engine setup.

Hardened (2026-08): the original Supabase project backing this app was deleted,
which took the whole API down - `create_db_and_tables()` runs inside the FastAPI
lifespan, so an unreachable Postgres meant the app failed to start rather than
merely losing persistence. This module now:

  * normalises the DATABASE_URL (postgres:// -> postgresql://, and percent-encodes
    a password that was pasted raw, which is the other way these URLs break),
  * probes the database once at import time, and
  * falls back to a local SQLite file if Postgres is unset or unreachable,
    so the service always boots and always serves.

Set DATABASE_URL to a live Postgres instance to get real persistence back.
"""

import os
import re
import tempfile
import urllib.parse

from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv

load_dotenv()


def _normalise(url: str) -> str:
    """Make a hand-pasted Postgres URL safe to parse."""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    # Supabase hands you `postgresql://user:[YOUR-PASSWORD]@host/db`. If the
    # password is pasted between those brackets, or contains #/&/@/?, the URL
    # is unparseable. Strip the brackets and percent-encode the password.
    m = re.match(r"^(?P<scheme>[a-z+]+://)(?P<user>[^:/@]+):(?P<pw>.*)@(?P<rest>[^@]+)$", url)
    if m:
        pw = m.group("pw")
        if pw.startswith("[") and pw.endswith("]"):
            pw = pw[1:-1]
        pw = urllib.parse.quote(urllib.parse.unquote(pw), safe="")
        url = f"{m.group('scheme')}{m.group('user')}:{pw}@{m.group('rest')}"
    return url


def _sqlite_fallback() -> str:
    """A SQLite path that is writable both locally and on serverless hosts."""
    local = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")
    try:
        # Vercel/Lambda filesystems are read-only apart from /tmp.
        with open(local, "a"):
            pass
        return f"sqlite:///{local}"
    except OSError:
        return f"sqlite:///{os.path.join(tempfile.gettempdir(), 'stock_news.db')}"


def _usable(url: str) -> bool:
    """Return True if we can actually open a connection to `url`."""
    try:
        probe = create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 10})
        with probe.connect():
            return True
    except Exception as exc:  # noqa: BLE001 - any failure means "fall back"
        print(f"WARNING: DATABASE_URL is not reachable ({type(exc).__name__}: {exc}). "
              f"Falling back to local SQLite so the API can still start.")
        return False


DATABASE_URL = os.getenv("DATABASE_URL", "").strip().strip('"')
USING_FALLBACK = False

if not DATABASE_URL:
    print("WARNING: No DATABASE_URL found. Using local SQLite.")
    DATABASE_URL, USING_FALLBACK = _sqlite_fallback(), True
else:
    DATABASE_URL = _normalise(DATABASE_URL)
    if not _usable(DATABASE_URL):
        DATABASE_URL, USING_FALLBACK = _sqlite_fallback(), True

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    """Create tables. Never raises - a DB outage must not stop the app booting."""
    try:
        SQLModel.metadata.create_all(engine)
        run_migrations()
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: could not create tables ({type(exc).__name__}: {exc}).")


_SQL_TYPES = {
    "INTEGER": "INTEGER", "BIGINT": "BIGINT", "VARCHAR": "VARCHAR",
    "TEXT": "TEXT", "DATETIME": "TIMESTAMP", "TIMESTAMP": "TIMESTAMP",
    "BOOLEAN": "BOOLEAN", "FLOAT": "FLOAT", "NUMERIC": "NUMERIC",
}


def run_migrations():
    """Add any model columns that are missing from existing tables.

    Replaces the manual `update_db.py` script, which had to be run by hand and
    therefore never ran on a deploy - that is why production tables drifted
    behind the models (e.g. `newsalert.image_url` missing). Reflecting the live
    schema and ALTERing in the gaps is idempotent and works on SQLite and
    Postgres alike. Never raises.
    """
    try:
        from sqlalchemy import inspect, text

        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())

        for table in SQLModel.metadata.sorted_tables:
            if table.name not in existing_tables:
                continue  # create_all() already made it with the full schema
            have = {c["name"] for c in inspector.get_columns(table.name)}
            for column in table.columns:
                if column.name in have or column.primary_key:
                    continue
                type_name = _SQL_TYPES.get(column.type.__class__.__name__.upper(), "VARCHAR")
                with engine.begin() as conn:
                    conn.execute(text(
                        f'ALTER TABLE {table.name} ADD COLUMN {column.name} {type_name}'
                    ))
                print(f"Migrated: added {table.name}.{column.name}")
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: schema migration skipped ({type(exc).__name__}: {exc}).")


def get_session():
    with Session(engine) as session:
        yield session
