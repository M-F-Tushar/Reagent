import sqlite3
from pathlib import Path

DEFAULT_DATABASE_PATH = Path("data/reagent.db")
_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect_database(database_path: str | Path = DEFAULT_DATABASE_PATH) -> sqlite3.Connection:
    """Open a SQLite database with foreign-key enforcement enabled."""
    is_memory_database = isinstance(database_path, str) and database_path == ":memory:"
    if not is_memory_database:
        Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection



def create_schema(connection: sqlite3.Connection) -> None:
    """Create the tables described by the Week 2 ER diagram."""
    connection.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))