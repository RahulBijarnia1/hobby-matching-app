"""
Hobby routes for managing hobbies.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hobby import Hobby
from app.schemas.hobby_schema import HobbyResponse, HobbyCreate

router = APIRouter()


@router.get(
    "",
    response_model=List[HobbyResponse],
    summary="Get all hobbies",
    description="Retrieve a list of all available hobbies."
)
async def get_hobbies(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Get all available hobbies.
    
    Args:
        category: Optional category filter.
    
    Returns:
        List of all hobbies in the database.
    """
    query = db.query(Hobby)
    
    if category:
        query = query.filter(Hobby.category == category)
    
    hobbies = query.order_by(Hobby.category, Hobby.name).all()
    return hobbies


@router.get(
    "/categories",
    response_model=List[str],
    summary="Get all hobby categories",
    description="Retrieve a list of unique hobby categories."
)
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all unique hobby categories.
    
    Returns:
        List of unique category names.
    """
    categories = db.query(Hobby.category).distinct().filter(
        Hobby.category.isnot(None)
    ).all()
    
    return [c[0] for c in categories if c[0]]


@router.get(
    "/{hobby_id}",
    response_model=HobbyResponse,
    summary="Get hobby by ID",
    description="Retrieve a specific hobby by its ID."
)
async def get_hobby(hobby_id: int, db: Session = Depends(get_db)):
    """
    Get a specific hobby by ID.
    
    Args:
        hobby_id: The ID of the hobby to retrieve.
        
    Returns:
        The hobby with the specified ID.
        
    Raises:
        HTTPException: If hobby is not found.
    """
    hobby = db.query(Hobby).filter(Hobby.id == hobby_id).first()
    
    if not hobby:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobby with ID {hobby_id} not found"
        )
    
    return hobby
