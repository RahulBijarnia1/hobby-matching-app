# Hobby Connect - Hobby Matching Application

A full-stack hobby matching application that connects users based on shared interests. Built with FastAPI (Python) backend and Angular frontend, featuring JWT authentication and a sophisticated matching algorithm.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Angular](https://img.shields.io/badge/angular-19-red.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.115+-green.svg)

## Features

### Authentication & Security
- **JWT Authentication**: Secure token-based authentication with access and refresh tokens
- **Password Security**: Bcrypt-hashed passwords with secure verification
- **Protected Routes**: Angular route guards for authenticated/guest-only pages
- **HTTP Interceptors**: Automatic JWT header injection for API requests

### User Features
- **User Registration**: Create profiles with name, age, email, and multiple hobbies
- **Profile Management**: Update profile details and hobby preferences
- **Smart Matching**: Advanced algorithm-based matching with weighted scoring
- **Match Discovery**: View and filter potential hobby partners

### UI/UX
- **Modern Dark Theme**: Beautiful dark mode interface with gradient accents
- **Responsive Design**: Mobile-first design built with Tailwind CSS
- **Real-time Updates**: Dynamic content loading without page refreshes
- **Toast Notifications**: User-friendly feedback for actions
- **Loading States**: Elegant spinner components during data fetching

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI 0.115+** - Modern, fast web framework with automatic OpenAPI docs
- **SQLAlchemy 2.0** - ORM for database operations
- **MySQL** - Relational database
- **Pydantic** - Data validation and serialization
- **python-jose** - JWT token encoding/decoding
- **passlib** - Password hashing with bcrypt
- **python-dotenv** - Environment variable management
- **Uvicorn** - ASGI server

### Frontend
- **Angular 19** - TypeScript-based web framework
- **Tailwind CSS 4** - Utility-first CSS framework
- **Reactive Forms** - Form handling and validation
- **RxJS** - Reactive programming and state management
- **Angular Router** - Client-side routing with guards

## Project Structure

```
hobby-matching-app/
├── backend/
│   ├── app/
│   │   ├── main.py              # Application entry point & lifespan
│   │   ├── database.py          # Database configuration
│   │   ├── config.py            # Settings & environment config
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py          # User model
│   │   │   ├── hobby.py         # Hobby model
│   │   │   └── user_hobby.py    # User-Hobby junction
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── auth_schema.py   # Auth request/response
│   │   │   ├── user_schema.py   # User schemas
│   │   │   └── hobby_schema.py  # Hobby schemas
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth_routes.py   # Authentication endpoints
│   │   │   ├── user_routes.py   # User management endpoints
│   │   │   └── hobby_routes.py  # Hobby endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── auth_service.py  # Auth & JWT logic
│   │   │   ├── user_service.py  # User operations
│   │   │   └── matching_service.py  # Matching algorithm
│   │   └── utils/               # Utility functions
│   │       ├── security.py      # Password & token utils
│   │       ├── validators.py    # Input validation
│   │       └── pagination.py    # Pagination helpers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── pages/           # Page components
│   │   │   │   ├── landing/     # Public landing page
│   │   │   │   ├── login/       # Login page
│   │   │   │   ├── register/    # Registration page
│   │   │   │   ├── dashboard/   # User dashboard
│   │   │   │   └── matches/     # Match discovery
│   │   │   ├── services/        # API services
│   │   │   │   ├── api.service.ts   # HTTP client
│   │   │   │   └── auth.service.ts  # Auth state management
│   │   │   ├── guards/          # Route guards
│   │   │   │   └── auth.guard.ts    # Auth & guest guards
│   │   │   ├── interceptors/    # HTTP interceptors
│   │   │   │   └── auth.interceptor.ts  # JWT injection
│   │   │   ├── shared/          # Shared components
│   │   │   │   ├── navbar/      # Navigation component
│   │   │   │   ├── spinner/     # Loading spinner
│   │   │   │   └── toast/       # Notification system
│   │   │   └── models/          # TypeScript interfaces
│   │   ├── environments/        # Environment configs
│   │   └── styles.css           # Global Tailwind styles
│   ├── tailwind.config.js
│   ├── angular.json
│   └── package.json
├── PROJECT_ARCHITECTURE.md
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- MySQL 8.0 or higher
- Git

### Database Setup

1. Create a MySQL database:
```sql
CREATE DATABASE hobby_matching_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file with your configuration:
```env
# Database
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/hobby_matching_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=development
```

6. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:4200`

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login (JSON body) | No |
| POST | `/api/v1/auth/login/form` | Login (form data) | No |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| POST | `/api/v1/auth/refresh` | Refresh access token | Yes |

### Users
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/users/profile` | Get current user profile | Yes |
| PUT | `/api/v1/users/profile` | Update profile | Yes |
| DELETE | `/api/v1/users/profile` | Delete account | Yes |
| GET | `/api/v1/users/matches` | Get hobby matches | Yes |
| GET | `/api/v1/users/hobbies` | Get user's hobbies | Yes |
| PUT | `/api/v1/users/hobbies` | Update user's hobbies | Yes |
| POST | `/api/v1/users/hobbies/{id}` | Add hobby to user | Yes |
| DELETE | `/api/v1/users/hobbies/{id}` | Remove hobby from user | Yes |

### Hobbies
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/hobbies` | Get all hobbies | No |
| GET | `/api/v1/hobbies/categories` | Get hobby categories | No |
| GET | `/api/v1/hobbies/{id}` | Get hobby by ID | No |

## Matching Algorithm

The matching algorithm uses a weighted formula to calculate compatibility:

```
match_score = (hobby_similarity × 0.70) + (age_proximity × 0.20) + (category_bonus × 0.10)
```

### Components

| Component | Weight | Description |
|-----------|--------|-------------|
| Hobby Similarity | 70% | Jaccard similarity coefficient of shared hobbies |
| Age Proximity | 20% | Closer ages score higher (within 10-year range) |
| Category Bonus | 10% | Bonus for matching hobby categories |

### Example

- User A (age 25): Photography, Hiking, Cooking, Gaming
- User B (age 27): Photography, Hiking, Reading, Music

Calculation:
- Hobby Similarity: 2 shared / 6 unique = 0.333 × 70 = 23.3%
- Age Proximity: |25-27| = 2 years → 80% × 20 = 16%
- Category Bonus: 2 category matches × 5% = 10%
- **Total: 49.3% match**

## Pre-seeded Hobbies

The application comes with 50+ pre-seeded hobbies across 7 categories:

| Category | Hobbies |
|----------|---------|
| Sports & Fitness | Running, Swimming, Cycling, Yoga, Basketball, etc. |
| Creative Arts | Photography, Painting, Drawing, Writing, etc. |
| Music | Playing Guitar, Piano, Singing, DJing, etc. |
| Technology | Programming, Gaming, 3D Printing, etc. |
| Outdoor | Hiking, Camping, Fishing, Gardening, etc. |
| Social | Dancing, Cooking, Board Games, Volunteering, etc. |
| Intellectual | Reading, Chess, Language Learning, etc. |

## Frontend Routes

| Route | Component | Guard | Description |
|-------|-----------|-------|-------------|
| `/` | Landing | Guest | Public landing page |
| `/login` | Login | Guest | User login |
| `/register` | Register | Guest | User registration |
| `/dashboard` | Dashboard | Auth | User dashboard |
| `/matches` | Matches | Auth | Match discovery |

## Deployment

### Backend (Render/Railway)

1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - `ENVIRONMENT=production`

### Frontend (Vercel/Netlify)

1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist/hobby-matching-frontend/browser`
4. Update `environment.prod.ts` with production API URL

## Environment Variables

### Backend
| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | MySQL connection string | Required |
| SECRET_KEY | JWT signing key (32+ chars) | Required |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token TTL | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token TTL | 7 |
| ENVIRONMENT | development/production | development |

### Frontend
| Variable | Description |
|----------|-------------|
| apiUrl | Backend API URL |
| production | Production flag |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Angular](https://angular.io/) - TypeScript web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [python-jose](https://python-jose.readthedocs.io/) - JWT implementation
