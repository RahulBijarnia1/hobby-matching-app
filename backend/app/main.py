"""
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, SessionLocal
from app.routes import user_routes, hobby_routes, auth_routes
from app.models.hobby import Hobby


# Default hobbies with categories
DEFAULT_HOBBIES = [
    # Sports & Fitness (20)
    {"name": "Soccer", "category": "Sports & Fitness"},
    {"name": "Basketball", "category": "Sports & Fitness"},
    {"name": "Tennis", "category": "Sports & Fitness"},
    {"name": "Swimming", "category": "Sports & Fitness"},
    {"name": "Running", "category": "Sports & Fitness"},
    {"name": "Yoga", "category": "Sports & Fitness"},
    {"name": "Gym & Weightlifting", "category": "Sports & Fitness"},
    {"name": "Cycling", "category": "Sports & Fitness"},
    {"name": "Hiking", "category": "Sports & Fitness"},
    {"name": "Martial Arts", "category": "Sports & Fitness"},
    {"name": "Cricket", "category": "Sports & Fitness"},
    {"name": "Badminton", "category": "Sports & Fitness"},
    {"name": "Table Tennis", "category": "Sports & Fitness"},
    {"name": "Volleyball", "category": "Sports & Fitness"},
    {"name": "Baseball", "category": "Sports & Fitness"},
    {"name": "Golf", "category": "Sports & Fitness"},
    {"name": "Boxing", "category": "Sports & Fitness"},
    {"name": "Skateboarding", "category": "Sports & Fitness"},
    {"name": "Rugby", "category": "Sports & Fitness"},
    {"name": "Ice Skating", "category": "Sports & Fitness"},
    
    # Arts & Creativity (15)
    {"name": "Painting", "category": "Arts & Creativity"},
    {"name": "Drawing", "category": "Arts & Creativity"},
    {"name": "Photography", "category": "Arts & Creativity"},
    {"name": "Writing", "category": "Arts & Creativity"},
    {"name": "Music Production", "category": "Arts & Creativity"},
    {"name": "Playing Guitar", "category": "Arts & Creativity"},
    {"name": "Playing Piano", "category": "Arts & Creativity"},
    {"name": "Singing", "category": "Arts & Creativity"},
    {"name": "Dancing", "category": "Arts & Creativity"},
    {"name": "Crafts & DIY", "category": "Arts & Creativity"},
    {"name": "Pottery", "category": "Arts & Creativity"},
    {"name": "Calligraphy", "category": "Arts & Creativity"},
    {"name": "Sculpting", "category": "Arts & Creativity"},
    {"name": "Knitting & Crochet", "category": "Arts & Creativity"},
    {"name": "Film Making", "category": "Arts & Creativity"},
    
    # Technology (12)
    {"name": "Programming", "category": "Technology"},
    {"name": "Gaming", "category": "Technology"},
    {"name": "3D Printing", "category": "Technology"},
    {"name": "Robotics", "category": "Technology"},
    {"name": "Web Development", "category": "Technology"},
    {"name": "Mobile App Development", "category": "Technology"},
    {"name": "AI & Machine Learning", "category": "Technology"},
    {"name": "Cybersecurity", "category": "Technology"},
    {"name": "Drone Flying", "category": "Technology"},
    {"name": "Game Development", "category": "Technology"},
    {"name": "Data Science", "category": "Technology"},
    {"name": "Electronics & Arduino", "category": "Technology"},
    
    # Entertainment (12)
    {"name": "Movies", "category": "Entertainment"},
    {"name": "TV Series", "category": "Entertainment"},
    {"name": "Anime", "category": "Entertainment"},
    {"name": "Reading", "category": "Entertainment"},
    {"name": "Board Games", "category": "Entertainment"},
    {"name": "Podcasts", "category": "Entertainment"},
    {"name": "Stand-up Comedy", "category": "Entertainment"},
    {"name": "Card Games", "category": "Entertainment"},
    {"name": "Trivia & Quiz", "category": "Entertainment"},
    {"name": "Cosplay", "category": "Entertainment"},
    {"name": "Magic & Illusion", "category": "Entertainment"},
    {"name": "Karaoke", "category": "Entertainment"},
    
    # Outdoor & Nature (13)
    {"name": "Camping", "category": "Outdoor & Nature"},
    {"name": "Fishing", "category": "Outdoor & Nature"},
    {"name": "Bird Watching", "category": "Outdoor & Nature"},
    {"name": "Gardening", "category": "Outdoor & Nature"},
    {"name": "Traveling", "category": "Outdoor & Nature"},
    {"name": "Rock Climbing", "category": "Outdoor & Nature"},
    {"name": "Surfing", "category": "Outdoor & Nature"},
    {"name": "Kayaking", "category": "Outdoor & Nature"},
    {"name": "Horseback Riding", "category": "Outdoor & Nature"},
    {"name": "Scuba Diving", "category": "Outdoor & Nature"},
    {"name": "Skiing & Snowboarding", "category": "Outdoor & Nature"},
    {"name": "Photography Nature Walks", "category": "Outdoor & Nature"},
    {"name": "Stargazing", "category": "Outdoor & Nature"},
    
    # Food & Culinary (10)
    {"name": "Cooking", "category": "Food & Culinary"},
    {"name": "Baking", "category": "Food & Culinary"},
    {"name": "Wine Tasting", "category": "Food & Culinary"},
    {"name": "Coffee Brewing", "category": "Food & Culinary"},
    {"name": "Food Photography", "category": "Food & Culinary"},
    {"name": "BBQ & Grilling", "category": "Food & Culinary"},
    {"name": "Mixology & Cocktails", "category": "Food & Culinary"},
    {"name": "Meal Prep", "category": "Food & Culinary"},
    {"name": "Tea Tasting", "category": "Food & Culinary"},
    {"name": "Fermentation & Pickling", "category": "Food & Culinary"},
    
    # Social & Community (10)
    {"name": "Volunteering", "category": "Social & Community"},
    {"name": "Event Planning", "category": "Social & Community"},
    {"name": "Public Speaking", "category": "Social & Community"},
    {"name": "Networking", "category": "Social & Community"},
    {"name": "Language Learning", "category": "Social & Community"},
    {"name": "Book Club", "category": "Social & Community"},
    {"name": "Debate & Discussion", "category": "Social & Community"},
    {"name": "Mentoring", "category": "Social & Community"},
    {"name": "Community Service", "category": "Social & Community"},
    {"name": "Cultural Exchange", "category": "Social & Community"},
    
    # Mind & Wellness (10)
    {"name": "Meditation", "category": "Mind & Wellness"},
    {"name": "Journaling", "category": "Mind & Wellness"},
    {"name": "Chess", "category": "Mind & Wellness"},
    {"name": "Puzzles & Sudoku", "category": "Mind & Wellness"},
    {"name": "Astrology", "category": "Mind & Wellness"},
    {"name": "Tarot & Oracle", "category": "Mind & Wellness"},
    {"name": "Mindfulness", "category": "Mind & Wellness"},
    {"name": "Aromatherapy", "category": "Mind & Wellness"},
    {"name": "Spa & Self-Care", "category": "Mind & Wellness"},
    {"name": "Breathwork", "category": "Mind & Wellness"},
    
    # Collecting & Hobbies (8)
    {"name": "Stamp Collecting", "category": "Collecting & Hobbies"},
    {"name": "Coin Collecting", "category": "Collecting & Hobbies"},
    {"name": "Vintage & Thrifting", "category": "Collecting & Hobbies"},
    {"name": "Model Building", "category": "Collecting & Hobbies"},
    {"name": "Lego Building", "category": "Collecting & Hobbies"},
    {"name": "Trading Cards", "category": "Collecting & Hobbies"},
    {"name": "Vinyl Records", "category": "Collecting & Hobbies"},
    {"name": "Antique Hunting", "category": "Collecting & Hobbies"},
]


def seed_hobbies():
    """Seed default hobbies if table is empty."""
    db = SessionLocal()
    try:
        existing = db.query(Hobby).count()
        if existing == 0:
            for hobby_data in DEFAULT_HOBBIES:
                hobby = Hobby(name=hobby_data["name"], category=hobby_data["category"])
                db.add(hobby)
            db.commit()
            print(f"Seeded {len(DEFAULT_HOBBIES)} hobbies.")
    except Exception as e:
        print(f"Error seeding hobbies: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("Initializing database...")
    init_db()
    seed_hobbies()
    print("Hobby Connect API started successfully!")
    yield
    # Shutdown
    print("Application shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A hobby matching application that connects users based on shared interests. Features JWT authentication, smart matching algorithm, and comprehensive user profiles.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth_routes.router,
    prefix=f"{settings.API_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    user_routes.router,
    prefix=f"{settings.API_PREFIX}/users",
    tags=["Users"]
)

app.include_router(
    hobby_routes.router,
    prefix=f"{settings.API_PREFIX}/hobbies",
    tags=["Hobbies"]
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Welcome to Hobby Connect API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
