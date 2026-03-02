"""
Hobby model definition.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.user_hobby import user_hobbies


class Hobby(Base):
    """Hobby model representing available hobbies."""
    
    __tablename__ = "hobbies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=True)
    
    # Many-to-many relationship with users
    users = relationship(
        "User",
        secondary=user_hobbies,
        back_populates="hobbies",
        lazy="select"
    )
    
    def __repr__(self):
        return f"<Hobby(id={self.id}, name='{self.name}', category='{self.category}')>"
