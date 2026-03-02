"""
User routes for managing users and matches.
"""

from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.hobby import Hobby
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserWithHobbies,
    UserMatchResponse
)
from app.services.matching_service import MatchingService
from app.services.user_service import UserService
from app.utils.security import get_current_user

router = APIRouter()


@router.get(
    "/profile",
    response_model=UserWithHobbies,
    summary="Get current user profile",
    description="Get the authenticated user's profile."
)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's profile.
    
    Returns:
        The user's profile with hobbies.
    """
    return current_user


@router.put(
    "/profile",
    response_model=UserWithHobbies,
    summary="Update current user profile",
    description="Update the authenticated user's profile."
)
async def update_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile.
    
    Args:
        update_data: The profile update data.
        
    Returns:
        The updated user profile.
    """
    user_service = UserService(db)
    
    try:
        updated_user = user_service.update_user(current_user, update_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return updated_user


@router.post(
    "/profile/hobbies",
    response_model=UserWithHobbies,
    summary="Add hobbies to profile",
    description="Add hobbies to the authenticated user's profile."
)
async def add_hobbies(
    hobby_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add hobbies to the current user's profile.
    
    Args:
        hobby_ids: List of hobby IDs to add.
        
    Returns:
        The updated user profile.
    """
    user_service = UserService(db)
    
    try:
        updated_user = user_service.add_hobbies_to_user(current_user, hobby_ids)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return updated_user


@router.delete(
    "/profile/hobbies",
    response_model=UserWithHobbies,
    summary="Remove hobbies from profile",
    description="Remove hobbies from the authenticated user's profile."
)
async def remove_hobbies(
    hobby_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove hobbies from the current user's profile.
    
    Args:
        hobby_ids: List of hobby IDs to remove.
        
    Returns:
        The updated user profile.
    """
    user_service = UserService(db)
    updated_user = user_service.remove_hobbies_from_user(current_user, hobby_ids)
    
    return updated_user


@router.get(
    "/matches",
    response_model=dict,
    summary="Get matched users",
    description="Find users with similar hobbies, sorted by match percentage."
)
async def get_matches(
    min_age: Optional[int] = Query(None, ge=13, le=150, description="Minimum age filter"),
    max_age: Optional[int] = Query(None, ge=13, le=150, description="Maximum age filter"),
    min_match_percentage: Optional[float] = Query(None, ge=0, le=100, description="Minimum match percentage"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=50, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get matched users based on hobby similarity.
    
    The match score is calculated as:
    - Common hobbies weight: 70%
    - Age proximity bonus: 20%
    - Same hobby category bonus: 10%
    
    Args:
        min_age: Optional minimum age filter.
        max_age: Optional maximum age filter.
        min_match_percentage: Optional minimum match percentage filter.
        page: Page number for pagination.
        page_size: Number of items per page.
        
    Returns:
        Paginated list of matched users sorted by match percentage.
    """
    matching_service = MatchingService(db)
    matches = matching_service.find_matches(
        user=current_user,
        min_age=min_age,
        max_age=max_age,
        min_match_percentage=min_match_percentage,
        page=page,
        page_size=page_size
    )
    
    return matches


@router.get(
    "",
    response_model=List[UserWithHobbies],
    summary="Get all users",
    description="Retrieve a list of all registered users."
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get all users with pagination.
    
    Args:
        skip: Number of records to skip.
        limit: Maximum number of records to return.
        
    Returns:
        List of users with their hobbies.
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get(
    "/{user_id}",
    response_model=UserWithHobbies,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID."
)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    Args:
        user_id: The ID of the user to retrieve.
        
    Returns:
        The user with the specified ID.
        
    Raises:
        HTTPException: If user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return user


@router.delete(
    "/account",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current user account",
    description="Delete the authenticated user's account."
)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete the current user's account.
    """
    db.delete(current_user)
    db.commit()
