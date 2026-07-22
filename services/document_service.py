"""
Document Service

This module contains the business logic for document operations.

Responsibilities:
- Validate document data
- Call repository methods
- Handle business rules
- Return processed results

The service layer should never directly interact with the database.
Instead, it communicates through the repository layer.
"""

from typing import List, Optional

from repositories.document_repository import DocumentRepository


class DocumentService:
    """
    Service class for document-related operations.

    This layer sits between:
        API Layer
            ↓
      DocumentService
            ↓
    DocumentRepository
            ↓
        Database
    """

    def __init__(self):
        """Initialize the service with a document repository."""
        self.repository = DocumentRepository()

    def create_document(self, title: str, content: str):
        """
        Create a new document.

        Args:
            title (str): Document title.
            content (str): Document content.

        Returns:
            Document: Newly created document.
        """
        if not title.strip():
            raise ValueError("Document title cannot be empty.")

        if not content.strip():
            raise ValueError("Document content cannot be empty.")

        return self.repository.create(title=title, content=content)

    def get_document(self, document_id: int):
        """
        Retrieve a document by ID.

        Args:
            document_id (int): Document ID.

        Returns:
            Document or None
        """
        return self.repository.get_by_id(document_id)

    def get_all_documents(self):
        """
        Retrieve all documents.

        Returns:
            List[Document]
        """
        return self.repository.get_all()

    def update_document(
        self,
        document_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ):
        """
        Update an existing document.

        Args:
            document_id (int): Document ID.
            title (str, optional): New title.
            content (str, optional): New content.

        Returns:
            Updated Document
        """
        document = self.repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        return self.repository.update(
            document=document,
            title=title,
            content=content,
        )

    def delete_document(self, document_id: int):
        """
        Delete a document.

        Args:
            document_id (int): Document ID.

        Returns:
            bool
        """
        document = self.repository.get_by_id(document_id)

        if document is None:
            raise ValueError("Document not found.")

        self.repository.delete(document)

        return True