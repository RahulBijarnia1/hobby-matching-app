"""
Schemas package initialization.
"""

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWithHobbies,
    UserMatchResponse,
    MatchQueryParams
)
from app.schemas.hobby_schema import HobbyBase, HobbyCreate, HobbyResponse
from app.schemas.auth_schema import (
    Token,
    TokenData,
    UserRegister,
    UserLogin,
    AuthResponse
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse", 
    "UserWithHobbies",
    "UserMatchResponse",
    "MatchQueryParams",
    "HobbyBase",
    "HobbyCreate",
    "HobbyResponse",
    "Token",
    "TokenData",
    "UserRegister",
    "UserLogin",
    "AuthResponse"
]
