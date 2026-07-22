"""
Base Service

This module contains the BaseService class, which provides
common functionality for all business service classes.

Author: Anand Kumar
Project: PQ Assistant
"""

from sqlalchemy.orm import Session


class BaseService:
    """
    Base class for all services.

    Every service inherits from this class to gain
    access to the database session.
    """

    def __init__(self, db: Session):
        """
        Initialize the service.

        Args:
            db (Session):
                Active SQLAlchemy database session.
        """
        self.db = db