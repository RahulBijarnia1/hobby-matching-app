"""
User Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator

from app.schemas.hobby_schema import HobbyResponse


class UserBase(BaseModel):
    """Base user schema with common attributes."""
    
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    age: int = Field(..., ge=13, le=150, description="User's age")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=6, max_length=100, description="User's password")
    bio: Optional[str] = Field(None, max_length=500, description="User's bio")
    hobby_ids: List[int] = Field(
        default=[],
        description="List of hobby IDs to associate with user"
    )
    
    @field_validator('hobby_ids')
    @classmethod
    def validate_hobby_ids(cls, v):
        """Ensure hobby IDs are unique."""
        if len(v) != len(set(v)):
            raise ValueError('Duplicate hobby IDs are not allowed')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="User's full name")
    age: Optional[int] = Field(None, ge=13, le=150, description="User's age")
    bio: Optional[str] = Field(None, max_length=500, description="User's bio")
    hobby_ids: Optional[List[int]] = Field(None, description="List of hobby IDs")
    
    @field_validator('hobby_ids')
    @classmethod
    def validate_hobby_ids(cls, v):
        """Ensure hobby IDs are unique."""
        if v is not None and len(v) != len(set(v)):
            raise ValueError('Duplicate hobby IDs are not allowed')
        return v


class UserResponse(UserBase):
    """Schema for basic user response."""
    
    id: int = Field(..., description="User unique identifier")
    bio: Optional[str] = Field(None, description="User's bio")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True


class UserWithHobbies(UserResponse):
    """Schema for user response including hobbies."""
    
    hobbies: List[HobbyResponse] = Field(default=[], description="User's hobbies")


class UserMatchResponse(BaseModel):
    """Schema for user match response."""
    
    id: int = Field(..., description="Matched user's ID")
    name: str = Field(..., description="Matched user's name")
    age: int = Field(..., description="Matched user's age")
    email: str = Field(..., description="Matched user's email")
    bio: Optional[str] = Field(None, description="Matched user's bio")
    match_percentage: float = Field(..., ge=0, le=100, description="Match percentage")
    common_hobbies: List[HobbyResponse] = Field(
        default=[], 
        description="Hobbies in common"
    )
    
    class Config:
        from_attributes = True


class MatchQueryParams(BaseModel):
    """Query parameters for match filtering."""
    
    min_age: Optional[int] = Field(None, ge=13, le=150, description="Minimum age filter")
    max_age: Optional[int] = Field(None, ge=13, le=150, description="Maximum age filter")
    min_match_percentage: Optional[float] = Field(None, ge=0, le=100, description="Minimum match percentage")
    page: Optional[int] = Field(1, ge=1, description="Page number")
    page_size: Optional[int] = Field(10, ge=1, le=50, description="Items per page")
