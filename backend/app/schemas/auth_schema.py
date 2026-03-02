"""
Authentication Pydantic schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    """JWT token response schema."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Token payload data schema."""
    
    user_id: Optional[int] = None
    email: Optional[str] = None


class UserRegister(BaseModel):
    """Schema for user registration."""
    
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    age: int = Field(..., ge=13, le=150, description="User's age (min 13)")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, max_length=100, description="User's password")
    bio: Optional[str] = Field(None, max_length=500, description="User's bio")


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class AuthResponse(BaseModel):
    """Schema for authentication response with user info."""
    
    id: int = Field(..., description="User ID")
    name: str = Field(..., description="User's name")
    email: str = Field(..., description="User's email")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    
    class Config:
        from_attributes = True
