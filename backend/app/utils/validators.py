"""
Custom validators for data validation.
"""

import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.
    
    Args:
        email: Email address to validate.
        
    Returns:
        True if email is valid, False otherwise.
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_age(age: int) -> bool:
    """
    Validate age is within acceptable range.
    
    Args:
        age: Age to validate.
        
    Returns:
        True if age is valid, False otherwise.
    """
    return 1 <= age <= 150


def validate_name(name: str) -> bool:
    """
    Validate name is not empty and within length limits.
    
    Args:
        name: Name to validate.
        
    Returns:
        True if name is valid, False otherwise.
    """
    if not name or not name.strip():
        return False
    return 1 <= len(name.strip()) <= 100


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """
    Sanitize string input by trimming whitespace.
    
    Args:
        value: String to sanitize.
        
    Returns:
        Sanitized string or None.
    """
    if value is None:
        return None
    return value.strip()
