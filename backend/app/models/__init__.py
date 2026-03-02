"""
Models package initialization.
"""

from app.models.user import User
from app.models.hobby import Hobby
from app.models.user_hobby import user_hobbies

__all__ = ["User", "Hobby", "user_hobbies"]
