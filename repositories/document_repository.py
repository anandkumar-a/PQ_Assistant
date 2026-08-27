"""
Repository for document-related database operations.
"""

from typing import Optional, List

from repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    """
    Handles CRUD operations for documents stored in SQLite.
    """

    def create_document(
        self,
        filename: str,
        file_type: str,
        file_path: str,
        content: str,
        metadata: Optional[str] = None,
    ) -> int:
        """
        Store a new document in the database.

        Returns:
            int: ID of the newly created document.
        """

        query = """
            INSERT INTO documents (
                filename,
                file_type,
                file_path,
                content,
                metadata
            )
            VALUES (?, ?, ?, ?, ?)
        """

        params = (
            filename,
            file_type,
            file_path,
            content,
            metadata,
        )

        return self.insert(query, params)

    def get_document_by_id(self, document_id: int) -> Optional[dict]:
        """
        Retrieve a document using its ID.
        """

        query = """
            SELECT *
            FROM documents
            WHERE id = ?
        """

        return self.fetch_one(query, (document_id,))

    def get_document_by_filename(
        self,
        filename: str,
    ) -> Optional[dict]:
        """
        Retrieve a document using its filename.
        """

        query = """
            SELECT *
            FROM documents
            WHERE filename = ?
        """

        return self.fetch_one(query, (filename,))

    def get_all_documents(self) -> List[dict]:
        """
        Retrieve all documents.
        """

        query = """
            SELECT *
            FROM documents
            ORDER BY id DESC
        """

        return self.fetch_all(query)

    def update_document(
        self,
        document_id: int,
        filename: str,
        file_type: str,
        file_path: str,
        content: str,
        metadata: Optional[str] = None,
    ) -> int:
        """
        Update an existing document.
        """

        query = """
            UPDATE documents
            SET
                filename = ?,
                file_type = ?,
                file_path = ?,
                content = ?,
                metadata = ?
            WHERE id = ?
        """

        params = (
            filename,
            file_type,
            file_path,
            content,
            metadata,
            document_id,
        )

        return self.execute(query, params)

    def delete_document(self, document_id: int) -> int:
        """
        Delete a document using its ID.
        """

        query = """
            DELETE FROM documents
            WHERE id = ?
        """

        return self.delete(query, (document_id,))

    def document_exists(self, filename: str) -> bool:
        """
        Check whether a document already exists.
        """

        query = """
            SELECT id
            FROM documents
            WHERE filename = ?
            LIMIT 1
        """

        result = self.fetch_one(query, (filename,))

        return result is not None

    def search_documents(self, keyword: str) -> List[dict]:
        """
        Search documents by filename or content.

        This is a basic SQL search.
        Semantic retrieval is handled separately by ChromaDB.
        """

        query = """
            SELECT *
            FROM documents
            WHERE filename LIKE ?
               OR content LIKE ?
            ORDER BY id DESC
        """

        search_term = f"%{keyword}%"

        return self.fetch_all(
            query,
            (search_term, search_term),
        )