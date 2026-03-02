"""
User-Hobby association table for many-to-many relationship.
"""

from sqlalchemy import Table, Column, Integer, ForeignKey

from app.database import Base

# Association table for many-to-many relationship between users and hobbies
user_hobbies = Table(
    "user_hobbies",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("hobby_id", Integer, ForeignKey("hobbies.id", ondelete="CASCADE"), primary_key=True)
)
