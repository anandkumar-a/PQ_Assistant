from typing import Generic, TypeVar, Optional, List
from database.sqlite.connection import DatabaseConnection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Base repository providing common database operations.

    All specific repositories such as DocumentRepository
    and QueryRepository inherit from this class.
    """

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]:
        """
        Execute a SELECT query and return a single record.
        """
        connection = self.db.get_connection()

        cursor = connection.cursor()
        cursor.execute(query, params)

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    def fetch_all(self, query: str, params: tuple = ()) -> List[dict]:
        """
        Execute a SELECT query and return all records.
        """
        connection = self.db.get_connection()

        cursor = connection.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    def execute(self, query: str, params: tuple = ()) -> int:
        """
        Execute INSERT, UPDATE, or DELETE query.

        Returns:
            int: Number of affected rows.
        """
        connection = self.db.get_connection()

        cursor = connection.cursor()
        cursor.execute(query, params)

        connection.commit()

        return cursor.rowcount

    def insert(self, query: str, params: tuple = ()) -> int:
        """
        Execute an INSERT query and return the generated row ID.
        """
        connection = self.db.get_connection()

        cursor = connection.cursor()
        cursor.execute(query, params)

        connection.commit()

        return cursor.lastrowid

    def delete(self, query: str, params: tuple = ()) -> int:
        """
        Execute a DELETE query.
        """
        return self.execute(query, params)