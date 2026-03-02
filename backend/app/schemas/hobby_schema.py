"""
Hobby Pydantic schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class HobbyBase(BaseModel):
    """Base hobby schema with common attributes."""
    
    name: str = Field(..., min_length=1, max_length=100, description="Hobby name")
    category: Optional[str] = Field(None, max_length=50, description="Hobby category")


class HobbyCreate(HobbyBase):
    """Schema for creating a new hobby."""
    pass


class HobbyResponse(BaseModel):
    """Schema for hobby response."""
    
    id: int = Field(..., description="Hobby unique identifier")
    name: str = Field(..., description="Hobby name")
    category: Optional[str] = Field(None, description="Hobby category")
    
    class Config:
        from_attributes = True
