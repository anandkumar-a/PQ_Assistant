"""
Repository for query-related database operations.
"""

from typing import Optional, List

from repositories.base_repository import BaseRepository


class QueryRepository(BaseRepository):
    """
    Handles CRUD operations for user queries and responses.
    """

    def create_query(
        self,
        query_text: str,
        intent: Optional[str] = None,
        response: Optional[str] = None,
        validation_status: Optional[str] = None,
    ) -> int:
        """
        Store a new user query.

        Returns:
            int: ID of the newly created query.
        """

        query = """
            INSERT INTO queries (
                query_text,
                intent,
                response,
                validation_status
            )
            VALUES (?, ?, ?, ?)
        """

        params = (
            query_text,
            intent,
            response,
            validation_status,
        )

        return self.insert(query, params)

    def get_query_by_id(
        self,
        query_id: int,
    ) -> Optional[dict]:
        """
        Retrieve a query using its ID.
        """

        query = """
            SELECT *
            FROM queries
            WHERE id = ?
        """

        return self.fetch_one(query, (query_id,))

    def get_all_queries(self) -> List[dict]:
        """
        Retrieve all stored queries.
        """

        query = """
            SELECT *
            FROM queries
            ORDER BY id DESC
        """

        return self.fetch_all(query)

    def update_query_response(
        self,
        query_id: int,
        response: str,
    ) -> int:
        """
        Update the generated response for a query.
        """

        query = """
            UPDATE queries
            SET response = ?
            WHERE id = ?
        """

        return self.execute(
            query,
            (response, query_id),
        )

    def update_validation_status(
        self,
        query_id: int,
        validation_status: str,
    ) -> int:
        """
        Update the validation status of a query.
        """

        query = """
            UPDATE queries
            SET validation_status = ?
            WHERE id = ?
        """

        return self.execute(
            query,
            (validation_status, query_id),
        )

    def get_queries_by_intent(
        self,
        intent: str,
    ) -> List[dict]:
        """
        Retrieve queries belonging to a specific intent.
        """

        query = """
            SELECT *
            FROM queries
            WHERE intent = ?
            ORDER BY id DESC
        """

        return self.fetch_all(query, (intent,))

    def get_queries_by_validation_status(
        self,
        validation_status: str,
    ) -> List[dict]:
        """
        Retrieve queries based on validation status.
        """

        query = """
            SELECT *
            FROM queries
            WHERE validation_status = ?
            ORDER BY id DESC
        """

        return self.fetch_all(
            query,
            (validation_status,),
        )

    def delete_query(self, query_id: int) -> int:
        """
        Delete a query using its ID.
        """

        query = """
            DELETE FROM queries
            WHERE id = ?
        """

        return self.delete(query, (query_id,))