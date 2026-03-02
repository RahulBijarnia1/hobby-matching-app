"""
Pagination utilities for API responses.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Parameters for pagination."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=10, ge=1, le=100, description="Items per page")
    
    @property
    def skip(self) -> int:
        """Calculate the number of records to skip."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get the limit (page size)."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""
    
    items: List[T] = Field(default=[], description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


def paginate(
    query: Query,
    page: int = 1,
    page_size: int = 10
) -> dict:
    """
    Apply pagination to a SQLAlchemy query.
    
    Args:
        query: The SQLAlchemy query to paginate.
        page: Current page number (1-indexed).
        page_size: Number of items per page.
        
    Returns:
        Dictionary containing paginated results and metadata.
    """
    # Get total count
    total = query.count()
    
    # Calculate pagination metadata
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    skip = (page - 1) * page_size
    
    # Get paginated items
    items = query.offset(skip).limit(page_size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }


def create_pagination_response(
    items: List[T],
    total: int,
    page: int,
    page_size: int
) -> dict:
    """
    Create a pagination response dictionary.
    
    Args:
        items: List of items for the current page.
        total: Total number of items.
        page: Current page number.
        page_size: Number of items per page.
        
    Returns:
        Dictionary containing paginated results and metadata.
    """
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
