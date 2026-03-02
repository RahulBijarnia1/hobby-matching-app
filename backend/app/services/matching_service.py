"""
Matching service for finding users with similar hobbies.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserMatchResponse
from app.schemas.hobby_schema import HobbyResponse


class MatchingService:
    """
    Service for calculating and finding user matches based on hobby similarity.
    
    Match Score Formula:
    - Common hobbies weight: 70%
    - Age proximity bonus: 20%
    - Same hobby category bonus: 10%
    """
    
    # Weights for match score calculation
    HOBBY_WEIGHT = 0.70
    AGE_WEIGHT = 0.20
    CATEGORY_WEIGHT = 0.10
    
    def __init__(self, db: Session):
        """
        Initialize the matching service.
        
        Args:
            db: Database session.
        """
        self.db = db
    
    def calculate_hobby_score(
        self, 
        user_hobbies: set, 
        other_hobbies: set
    ) -> float:
        """
        Calculate the hobby similarity score between two users.
        
        Formula: (common hobbies / current user's total hobbies) * 100
        
        Args:
            user_hobbies: Set of hobby IDs for the current user.
            other_hobbies: Set of hobby IDs for the other user.
            
        Returns:
            Hobby score as a float between 0 and 100.
        """
        if not user_hobbies:
            return 0.0
        
        common_hobbies = user_hobbies.intersection(other_hobbies)
        return (len(common_hobbies) / len(user_hobbies)) * 100
    
    def calculate_age_proximity_score(
        self, 
        user_age: int, 
        other_age: int,
        max_age_diff: int = 30
    ) -> float:
        """
        Calculate age proximity score.
        
        Closer ages get higher scores.
        
        Args:
            user_age: Current user's age.
            other_age: Other user's age.
            max_age_diff: Maximum age difference for scoring (default: 30).
            
        Returns:
            Age proximity score as a float between 0 and 100.
        """
        age_diff = abs(user_age - other_age)
        
        if age_diff >= max_age_diff:
            return 0.0
        
        return ((max_age_diff - age_diff) / max_age_diff) * 100
    
    def calculate_category_score(
        self, 
        user_hobby_categories: set, 
        other_hobby_categories: set
    ) -> float:
        """
        Calculate category match score.
        
        Args:
            user_hobby_categories: Set of hobby categories for the current user.
            other_hobby_categories: Set of hobby categories for the other user.
            
        Returns:
            Category score as a float between 0 and 100.
        """
        if not user_hobby_categories:
            return 0.0
        
        # Remove None values
        user_categories = {c for c in user_hobby_categories if c}
        other_categories = {c for c in other_hobby_categories if c}
        
        if not user_categories:
            return 50.0  # Neutral score if no categories defined
        
        common_categories = user_categories.intersection(other_categories)
        return (len(common_categories) / len(user_categories)) * 100
    
    def calculate_match_percentage(
        self,
        user: User,
        other_user: User
    ) -> float:
        """
        Calculate the overall match percentage between two users.
        
        Formula:
        score = (hobby_score * 0.70) + (age_score * 0.20) + (category_score * 0.10)
        
        Args:
            user: The current user.
            other_user: The other user to compare with.
            
        Returns:
            Match percentage as a float between 0 and 100.
        """
        # Get hobby IDs
        user_hobby_ids = {h.id for h in user.hobbies}
        other_hobby_ids = {h.id for h in other_user.hobbies}
        
        # Get hobby categories
        user_categories = {h.category for h in user.hobbies}
        other_categories = {h.category for h in other_user.hobbies}
        
        # Calculate individual scores
        hobby_score = self.calculate_hobby_score(user_hobby_ids, other_hobby_ids)
        age_score = self.calculate_age_proximity_score(user.age, other_user.age)
        category_score = self.calculate_category_score(user_categories, other_categories)
        
        # Calculate weighted total
        total_score = (
            (hobby_score * self.HOBBY_WEIGHT) +
            (age_score * self.AGE_WEIGHT) +
            (category_score * self.CATEGORY_WEIGHT)
        )
        
        return round(total_score, 2)
    
    def get_common_hobbies(
        self, 
        user: User, 
        other_user: User
    ) -> List[HobbyResponse]:
        """
        Get the list of common hobbies between two users.
        
        Args:
            user: The current user.
            other_user: The other user to compare with.
            
        Returns:
            List of common hobby responses.
        """
        user_hobby_ids = {h.id for h in user.hobbies}
        common = [
            HobbyResponse(id=h.id, name=h.name, category=h.category)
            for h in other_user.hobbies 
            if h.id in user_hobby_ids
        ]
        return common
    
    def find_matches(
        self,
        user: User,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        min_match_percentage: Optional[float] = None,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        """
        Find all matching users sorted by match percentage with pagination.
        
        Args:
            user: The user to find matches for.
            min_age: Optional minimum age filter.
            max_age: Optional maximum age filter.
            min_match_percentage: Optional minimum match percentage filter.
            page: Page number for pagination.
            page_size: Number of items per page.
            
        Returns:
            Dictionary containing paginated matched users and metadata.
        """
        # Build query for other users
        query = self.db.query(User).filter(User.id != user.id)
        
        # Apply age filters if provided
        if min_age is not None:
            query = query.filter(User.age >= min_age)
        if max_age is not None:
            query = query.filter(User.age <= max_age)
        
        other_users = query.all()
        
        # Get current user's hobby IDs
        user_hobby_ids = {h.id for h in user.hobbies}
        
        # Calculate matches
        matches = []
        for other_user in other_users:
            other_hobby_ids = {h.id for h in other_user.hobbies}
            
            # Skip users with no common hobbies
            common_hobby_ids = user_hobby_ids.intersection(other_hobby_ids)
            if not common_hobby_ids:
                continue
            
            match_percentage = self.calculate_match_percentage(user, other_user)
            
            # Apply minimum match percentage filter
            if min_match_percentage is not None and match_percentage < min_match_percentage:
                continue
            
            common_hobbies = self.get_common_hobbies(user, other_user)
            
            match_response = UserMatchResponse(
                id=other_user.id,
                name=other_user.name,
                age=other_user.age,
                email=other_user.email,
                bio=other_user.bio,
                match_percentage=match_percentage,
                common_hobbies=common_hobbies
            )
            matches.append(match_response)
        
        # Sort by match percentage (descending)
        matches.sort(key=lambda x: x.match_percentage, reverse=True)
        
        # Apply pagination
        total = len(matches)
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_matches = matches[start_idx:end_idx]
        
        return {
            "items": paginated_matches,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
