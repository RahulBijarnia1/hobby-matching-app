"""
User service for user management operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.hobby import Hobby
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.security import get_password_hash


class UserService:
    """
    Service for handling user management operations.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the user service.
        
        Args:
            db: Database session.
        """
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            user_id: The user ID to search for.
            
        Returns:
            User if found, None otherwise.
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        
        Args:
            email: The email address to search for.
            
        Returns:
            User if found, None otherwise.
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all_users(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
            
        Returns:
            List of users.
        """
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data.
            
        Returns:
            The created User object.
            
        Raises:
            ValueError: If email already exists or hobbies not found.
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash the password
        hashed_password = get_password_hash(user_data.password)
        
        # Get hobbies if provided
        hobbies = []
        if user_data.hobby_ids:
            hobbies = self.db.query(Hobby).filter(
                Hobby.id.in_(user_data.hobby_ids)
            ).all()
            
            if len(hobbies) != len(user_data.hobby_ids):
                found_ids = {h.id for h in hobbies}
                missing_ids = set(user_data.hobby_ids) - found_ids
                raise ValueError(f"Hobbies with IDs {missing_ids} not found")
        
        # Create user
        user = User(
            name=user_data.name,
            age=user_data.age,
            email=user_data.email,
            hashed_password=hashed_password,
            bio=user_data.bio
        )
        user.hobbies = hobbies
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user(self, user: User, update_data: UserUpdate) -> User:
        """
        Update a user's profile.
        
        Args:
            user: The user to update.
            update_data: The update data.
            
        Returns:
            The updated User object.
            
        Raises:
            ValueError: If hobbies not found.
        """
        # Update basic fields
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.age is not None:
            user.age = update_data.age
        if update_data.bio is not None:
            user.bio = update_data.bio
        
        # Update hobbies if provided
        if update_data.hobby_ids is not None:
            hobbies = self.db.query(Hobby).filter(
                Hobby.id.in_(update_data.hobby_ids)
            ).all()
            
            if len(hobbies) != len(update_data.hobby_ids):
                found_ids = {h.id for h in hobbies}
                missing_ids = set(update_data.hobby_ids) - found_ids
                raise ValueError(f"Hobbies with IDs {missing_ids} not found")
            
            user.hobbies = hobbies
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user: User) -> None:
        """
        Delete a user.
        
        Args:
            user: The user to delete.
        """
        self.db.delete(user)
        self.db.commit()
    
    def add_hobbies_to_user(
        self, 
        user: User, 
        hobby_ids: List[int]
    ) -> User:
        """
        Add hobbies to a user.
        
        Args:
            user: The user to add hobbies to.
            hobby_ids: List of hobby IDs to add.
            
        Returns:
            The updated User object.
            
        Raises:
            ValueError: If hobbies not found.
        """
        hobbies = self.db.query(Hobby).filter(Hobby.id.in_(hobby_ids)).all()
        
        if len(hobbies) != len(hobby_ids):
            found_ids = {h.id for h in hobbies}
            missing_ids = set(hobby_ids) - found_ids
            raise ValueError(f"Hobbies with IDs {missing_ids} not found")
        
        # Add new hobbies (avoiding duplicates)
        current_hobby_ids = {h.id for h in user.hobbies}
        for hobby in hobbies:
            if hobby.id not in current_hobby_ids:
                user.hobbies.append(hobby)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def remove_hobbies_from_user(
        self, 
        user: User, 
        hobby_ids: List[int]
    ) -> User:
        """
        Remove hobbies from a user.
        
        Args:
            user: The user to remove hobbies from.
            hobby_ids: List of hobby IDs to remove.
            
        Returns:
            The updated User object.
        """
        user.hobbies = [h for h in user.hobbies if h.id not in hobby_ids]
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
