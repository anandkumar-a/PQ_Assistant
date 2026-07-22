from __future__ import annotations

import sqlite3

from .connection import SQLiteConnection


class DatabaseBase:
    """
    Base class for database components.

    Provides a reusable SQLite connection and common
    database utility methods.
    """

    def __init__(self) -> None:
        """
        Initialize the database connection and cursor.
        """
        self.connection: sqlite3.Connection = SQLiteConnection.get_connection()
        self.cursor: sqlite3.Cursor = self.connection.cursor()

    def commit(self) -> None:
        """
        Commit the current transaction.
        """
        self.connection.commit()

    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        self.connection.rollback()

    def close(self) -> None:
        """
        Close the database cursor and connection.
        """
        self.cursor.close()
        self.connection.close()