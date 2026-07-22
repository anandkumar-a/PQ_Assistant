from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteConnection:
    """
    Manages SQLite database connections for the application.
    """

    DATABASE_DIRECTORY = Path("data")
    DATABASE_NAME = "pq_assistant.db"

    @classmethod
    def get_database_path(cls) -> Path:
        """
        Returns the full path to the SQLite database file.
        Creates the data directory if it does not exist.
        """
        cls.DATABASE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        return cls.DATABASE_DIRECTORY / cls.DATABASE_NAME

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """
        Creates and returns a configured SQLite connection.
        """
        connection = sqlite3.connect(cls.get_database_path())

        # Access columns by name
        connection.row_factory = sqlite3.Row

        # Enable SQLite foreign key constraints
        connection.execute("PRAGMA foreign_keys = ON;")

        return connection