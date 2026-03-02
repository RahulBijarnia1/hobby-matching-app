"""
Authentication routes for user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    AuthResponse,
    Token
)
from app.schemas.user_schema import UserWithHobbies
from app.services.auth_service import AuthService
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and return authentication token."
)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data including name, age, email, password.
        
    Returns:
        Authentication response with access token.
        
    Raises:
        HTTPException: If email already exists.
    """
    auth_service = AuthService(db)
    
    try:
        user = auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create token for the new user
    access_token = auth_service.create_token_for_user(user)
    
    return AuthResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        access_token=access_token,
        token_type="bearer"
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="Authenticate user and return access token."
)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login a user.
    
    Args:
        login_data: User login credentials.
        
    Returns:
        Authentication response with access token.
        
    Raises:
        HTTPException: If credentials are invalid.
    """
    auth_service = AuthService(db)
    auth_response = auth_service.login_user(login_data)
    
    if not auth_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return auth_response


@router.post(
    "/login/form",
    response_model=Token,
    summary="Login user (OAuth2 form)",
    description="Authenticate user using OAuth2 form data."
)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login a user using OAuth2 form data.
    This endpoint is compatible with OAuth2PasswordBearer.
    
    Args:
        form_data: OAuth2 form data with username (email) and password.
        
    Returns:
        Token response with access token.
        
    Raises:
        HTTPException: If credentials are invalid.
    """
    auth_service = AuthService(db)
    
    # OAuth2 form uses 'username' field, but we use email
    login_data = UserLogin(email=form_data.username, password=form_data.password)
    auth_response = auth_service.login_user(login_data)
    
    if not auth_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(
        access_token=auth_response.access_token,
        token_type=auth_response.token_type
    )


@router.get(
    "/me",
    response_model=UserWithHobbies,
    summary="Get current user",
    description="Get the currently authenticated user's profile."
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current authenticated user's profile.
    
    Args:
        current_user: The authenticated user from JWT token.
        
    Returns:
        The user's profile with hobbies.
    """
    return current_user


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Get a new access token using current valid token."
)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresh the access token.
    
    Args:
        current_user: The authenticated user from JWT token.
        
    Returns:
        New token response with fresh access token.
    """
    auth_service = AuthService(db)
    access_token = auth_service.create_token_for_user(current_user)
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
