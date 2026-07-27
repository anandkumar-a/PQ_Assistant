"""
Query Service

This service contains the business logic for handling user queries.
It communicates with the QueryRepository and provides an abstraction
between the API layer and the database layer.
"""

from typing import List, Optional

from repositories.query_repository import QueryRepository
from services.base_service import BaseService


class QueryService(BaseService):
    """
    Service class for query-related operations.
    """

    def __init__(self):
        super().__init__()
        self.repository = QueryRepository()

    def create_query(self, query_data):
        """
        Store a new query.

        Args:
            query_data: Query model instance.

        Returns:
            Stored query object.
        """
        try:
            return self.repository.create(query_data)
        except Exception as e:
            self.logger.exception("Failed to create query.")
            raise e

    def get_query_by_id(self, query_id: int):
        """
        Retrieve a query using its ID.

        Args:
            query_id (int): Query identifier.

        Returns:
            Query object or None.
        """
        try:
            return self.repository.get_by_id(query_id)
        except Exception as e:
            self.logger.exception(f"Failed to retrieve query {query_id}.")
            raise e

    def get_all_queries(self) -> List:
        """
        Retrieve all stored queries.

        Returns:
            List of queries.
        """
        try:
            return self.repository.get_all()
        except Exception as e:
            self.logger.exception("Failed to retrieve queries.")
            raise e

    def update_query(self, query_id: int, updated_data):
        """
        Update an existing query.

        Args:
            query_id (int): Query identifier.
            updated_data: Updated query model.

        Returns:
            Updated query object.
        """
        try:
            return self.repository.update(query_id, updated_data)
        except Exception as e:
            self.logger.exception(f"Failed to update query {query_id}.")
            raise e

    def delete_query(self, query_id: int) -> bool:
        """
        Delete a query.

        Args:
            query_id (int): Query identifier.

        Returns:
            bool: True if deleted successfully.
        """
        try:
            return self.repository.delete(query_id)
        except Exception as e:
            self.logger.exception(f"Failed to delete query {query_id}.")
            raise e

    def search_queries(self, keyword: str):
        """
        Search queries by keyword.

        Args:
            keyword (str): Search text.

        Returns:
            List of matching queries.
        """
        try:
            return self.repository.search(keyword)
        except Exception as e:
            self.logger.exception("Query search failed.")
            raise e