"""
Base repository implementation.

This module provides a reusable repository with common CRUD operations.
Specific repositories should inherit from this class instead of
re-implementing database logic.
"""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from database.sqlite.base import Base

# Generic type representing a SQLAlchemy model
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable CRUD operations.
    """

    def __init__(self, session: Session, model: Type[ModelType]):
        """
        Initialize the repository.

        Args:
            session: SQLAlchemy database session.
            model: SQLAlchemy model class managed by this repository.
        """
        self.session = session
        self.model = model

    def create(self, entity: ModelType) -> ModelType:
        """
        Add a new entity to the database.
        """
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        """
        Retrieve an entity by its primary key.
        """
        return self.session.get(self.model, entity_id)

    def get_all(self) -> List[ModelType]:
        """
        Retrieve all records.
        """
        return self.session.query(self.model).all()

    def update(self, entity: ModelType) -> ModelType:
        """
        Update an existing entity.
        """
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: ModelType) -> None:
        """
        Delete an entity.
        """
        self.session.delete(entity)
        self.session.commit()

    def exists(self, entity_id: int) -> bool:
        """
        Check whether an entity exists.
        """
        return self.get_by_id(entity_id) is not None

    def count(self) -> int:
        """
        Count total records.
        """
        return self.session.query(self.model).count()