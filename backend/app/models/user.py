"""
User model
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base


class User(Base):
    """User account model - can be both host and venue owner"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # User preferences
    is_host = Column(Boolean, default=True)
    is_venue_owner = Column(Boolean, default=False)

    # Verification status
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
