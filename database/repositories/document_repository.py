"""
Document repository.

Provides database operations specific to the Document model.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from database.sqlite.models import Document

from .base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """
    Repository responsible for Document database operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the document repository.

        Args:
            session: Active SQLAlchemy session.
        """
        super().__init__(session, Document)

    def get_by_filename(self, filename: str) -> Optional[Document]:
        """
        Retrieve a document using its filename.

        Args:
            filename: Name of the document.

        Returns:
            Document if found, otherwise None.
        """
        return (
            self.session.query(Document)
            .filter(Document.filename == filename)
            .first()
        )

    def get_by_source(self, source: str) -> List[Document]:
        """
        Retrieve all documents from a given source.

        Args:
            source: Source name.

        Returns:
            List of matching documents.
        """
        return (
            self.session.query(Document)
            .filter(Document.source == source)
            .all()
        )

    def search_documents(self, keyword: str) -> List[Document]:
        """
        Search documents by filename.

        Args:
            keyword: Search keyword.

        Returns:
            List of matching documents.
        """
        return (
            self.session.query(Document)
            .filter(Document.filename.ilike(f"%{keyword}%"))
            .all()
        )

    def get_recent_documents(self, limit: int = 10) -> List[Document]:
        """
        Retrieve the most recently added documents.

        Args:
            limit: Maximum number of documents to return.

        Returns:
            List of recent documents.
        """
        return (
            self.session.query(Document)
            .order_by(Document.created_at.desc())
            .limit(limit)
            .all()
        )

    def delete_document(self, document_id: int) -> bool:
        """
        Delete a document by its ID.

        Args:
            document_id: Document identifier.

        Returns:
            True if deleted successfully, otherwise False.
        """
        document = self.get_by_id(document_id)

        if document is None:
            return False

        self.delete(document)
        return True