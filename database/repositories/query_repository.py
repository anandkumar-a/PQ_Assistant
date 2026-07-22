"""
Query repository.

Provides database operations specific to the Query model.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from database.sqlite.models import Query

from .base_repository import BaseRepository


class QueryRepository(BaseRepository[Query]):
    """
    Repository responsible for Query database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the query repository.

        Args:
            session: Active SQLAlchemy session.
        """
        super().__init__(session, Query)

    def get_by_query_text(self, query_text: str) -> Optional[Query]:
        """
        Retrieve a query by its exact text.

        Args:
            query_text: User query.

        Returns:
            Query object if found, otherwise None.
        """
        return (
            self.session.query(Query)
            .filter(Query.query_text == query_text)
            .first()
        )

    def search_queries(self, keyword: str) -> List[Query]:
        """
        Search queries containing a keyword.

        Args:
            keyword: Search keyword.

        Returns:
            List of matching queries.
        """
        return (
            self.session.query(Query)
            .filter(Query.query_text.ilike(f"%{keyword}%"))
            .all()
        )

    def get_recent_queries(self, limit: int = 10) -> List[Query]:
        """
        Retrieve the most recent queries.

        Args:
            limit: Maximum number of queries to return.

        Returns:
            List of recent queries.
        """
        return (
            self.session.query(Query)
            .order_by(Query.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_query_history(self) -> List[Query]:
        """
        Retrieve all queries ordered by most recent.

        Returns:
            List of queries.
        """
        return (
            self.session.query(Query)
            .order_by(Query.created_at.desc())
            .all()
        )

    def delete_query(self, query_id: int) -> bool:
        """
        Delete a query by its ID.

        Args:
            query_id: Query identifier.

        Returns:
            True if deleted successfully, otherwise False.
        """
        query = self.get_by_id(query_id)

        if query is None:
            return False

        self.delete(query)
        return True