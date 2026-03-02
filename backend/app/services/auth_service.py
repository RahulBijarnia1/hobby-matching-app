"""
Authentication service for user registration and login.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.hobby import Hobby
from app.schemas.auth_schema import UserRegister, UserLogin, AuthResponse
from app.utils.security import verify_password, get_password_hash, create_access_token


class AuthService:
    """
    Service for handling user authentication operations.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the auth service.
        
        Args:
            db: Database session.
        """
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        
        Args:
            email: The email address to search for.
            
        Returns:
            User if found, None otherwise.
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            email: User's email address.
            password: User's plain text password.
            
        Returns:
            User if authentication successful, None otherwise.
        """
        user = self.get_user_by_email(email)
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    def register_user(self, user_data: UserRegister) -> User:
        """
        Register a new user.
        
        Args:
            user_data: User registration data.
            
        Returns:
            The created User object.
            
        Raises:
            ValueError: If email already exists.
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = User(
            name=user_data.name,
            age=user_data.age,
            email=user_data.email,
            hashed_password=hashed_password,
            bio=user_data.bio
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def login_user(self, login_data: UserLogin) -> Optional[AuthResponse]:
        """
        Login a user and return auth response with token.
        
        Args:
            login_data: User login credentials.
            
        Returns:
            AuthResponse with token if successful, None otherwise.
        """
        user = self.authenticate_user(login_data.email, login_data.password)
        
        if not user:
            return None
        
        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return AuthResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            access_token=access_token,
            token_type="bearer"
        )
    
    def create_token_for_user(self, user: User) -> str:
        """
        Create an access token for a user.
        
        Args:
            user: The user to create a token for.
            
        Returns:
            The JWT access token string.
        """
        return create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
