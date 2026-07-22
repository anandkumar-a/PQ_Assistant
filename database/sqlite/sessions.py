from __future__ import annotations

import sqlite3
from typing import Any, Iterable, Optional

from .base import DatabaseBase
from .models import DatabaseModels


class DatabaseSession(DatabaseBase):
    """
    Manages database sessions and transactions.
    """

    def initialize_database(self) -> None:
        """
        Create all application tables if they do not exist.
        """
        try:
            for table in DatabaseModels.TABLES:
                self.cursor.execute(table)

            self.commit()

        except sqlite3.Error:
            self.rollback()
            raise

    def execute(
        self,
        query: str,
        parameters: Optional[Iterable[Any]] = None,
    ) -> sqlite3.Cursor:
        """
        Execute a SQL statement.
        """
        if parameters is None:
            return self.cursor.execute(query)

        return self.cursor.execute(query, tuple(parameters))

    def execute_many(
        self,
        query: str,
        parameters: Iterable[Iterable[Any]],
    ) -> sqlite3.Cursor:
        """
        Execute the same SQL statement for multiple parameter sets.
        """
        return self.cursor.executemany(query, parameters)

    def fetch_one(self):
        """
        Fetch a single row.
        """
        return self.cursor.fetchone()

    def fetch_all(self):
        """
        Fetch all rows.
        """
        return self.cursor.fetchall()