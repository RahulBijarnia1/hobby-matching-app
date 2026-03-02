"""
Routes package initialization.
"""

from app.routes.user_routes import router as user_router
from app.routes.hobby_routes import router as hobby_router
from app.routes.auth_routes import router as auth_router

__all__ = ["user_router", "hobby_router", "auth_router"]
