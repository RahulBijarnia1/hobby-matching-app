# Hobby Connect - Project Architecture

## Overview

**Hobby Connect** is a professional, full-stack hobby matching application that connects users based on shared interests. The application features JWT authentication, smart matching algorithms, and a modern responsive UI.

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Runtime environment |
| FastAPI | Modern async web framework |
| SQLAlchemy 2.0 | ORM for database operations |
| MySQL | Relational database |
| Pydantic | Data validation & serialization |
| python-jose | JWT token handling |
| passlib (bcrypt) | Password hashing |
| python-dotenv | Environment configuration |
| Uvicorn | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| Angular 19 | Frontend framework |
| TypeScript | Type-safe JavaScript |
| Tailwind CSS | Utility-first styling |
| RxJS | Reactive programming |
| Angular Router | Client-side routing |
| Reactive Forms | Form handling |

---

## Project Structure

```
hobby-matching-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Environment configuration
│   │   ├── database.py          # Database connection & session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py          # User SQLAlchemy model
│   │   │   ├── hobby.py         # Hobby SQLAlchemy model
│   │   │   └── user_hobby.py    # Association table
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth_schema.py   # Auth request/response schemas
│   │   │   ├── user_schema.py   # User schemas
│   │   │   └── hobby_schema.py  # Hobby schemas
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py   # /api/v1/auth endpoints
│   │   │   ├── user_routes.py   # /api/v1/users endpoints
│   │   │   └── hobby_routes.py  # /api/v1/hobbies endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py  # Authentication logic
│   │   │   ├── user_service.py  # User management logic
│   │   │   └── matching_service.py  # Matching algorithm
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py      # JWT & password utilities
│   │       ├── pagination.py    # Pagination helpers
│   │       └── validators.py    # Custom validators
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts/html/css
│   │   │   ├── app.config.ts
│   │   │   ├── app.routes.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts    # Route protection
│   │   │   ├── interceptors/
│   │   │   │   └── auth.interceptor.ts  # JWT header injection
│   │   │   ├── models/
│   │   │   │   └── models.ts        # TypeScript interfaces
│   │   │   ├── pages/
│   │   │   │   ├── landing/         # Public landing page
│   │   │   │   ├── login/           # Login page
│   │   │   │   ├── register/        # Registration page
│   │   │   │   ├── dashboard/       # User dashboard
│   │   │   │   └── matches/         # Match discovery
│   │   │   ├── services/
│   │   │   │   ├── api.service.ts   # API communication
│   │   │   │   └── auth.service.ts  # Auth state management
│   │   │   └── shared/
│   │   │       ├── navbar/          # Navigation component
│   │   │       ├── spinner/         # Loading spinner
│   │   │       └── toast/           # Toast notifications
│   │   ├── environments/
│   │   │   ├── environment.ts       # Development config
│   │   │   └── environment.prod.ts  # Production config
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.css               # Global Tailwind styles
│   ├── public/
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── angular.json
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── tsconfig.json
│
├── .gitignore
├── LICENSE
├── PROJECT_ARCHITECTURE.md
└── README.md
```

---

## Database Schema

### users
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | NOT NULL |
| age | INT | NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| bio | TEXT | NULLABLE |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### hobbies
| Column | Type | Constraints |
|--------|------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT |
| name | VARCHAR(100) | UNIQUE, NOT NULL |
| category | VARCHAR(50) | NULLABLE |

### user_hobbies (Junction Table)
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | INT | PRIMARY KEY, FOREIGN KEY → users.id |
| hobby_id | INT | PRIMARY KEY, FOREIGN KEY → hobbies.id |

---

## API Endpoints

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register new user | ❌ |
| POST | `/login` | Login and get token | ❌ |
| POST | `/login/form` | OAuth2 form login | ❌ |
| GET | `/me` | Get current user profile | ✅ |
| POST | `/refresh` | Refresh access token | ✅ |

### Users (`/api/v1/users`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/profile` | Get current user profile | ✅ |
| PUT | `/profile` | Update current user profile | ✅ |
| POST | `/profile/hobbies` | Add hobbies to profile | ✅ |
| DELETE | `/profile/hobbies` | Remove hobbies from profile | ✅ |
| GET | `/matches` | Get matched users | ✅ |
| GET | `/` | Get all users (paginated) | ❌ |
| GET | `/{user_id}` | Get user by ID | ❌ |
| DELETE | `/account` | Delete current user account | ✅ |

### Hobbies (`/api/v1/hobbies`)
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Get all hobbies | ❌ |
| GET | `/categories` | Get hobby categories | ❌ |
| GET | `/{hobby_id}` | Get hobby by ID | ❌ |

---

## Matching Algorithm

The matching score is calculated using a weighted formula:

```
Total Score = (Hobby Score × 0.70) + (Age Score × 0.20) + (Category Score × 0.10)
```

### Components

**1. Hobby Score (70% weight)**
```
hobby_score = (common_hobbies / user_total_hobbies) × 100
```

**2. Age Proximity Score (20% weight)**
```
age_diff = |user_age - other_age|
age_score = ((30 - age_diff) / 30) × 100  # Max diff: 30 years
```

**3. Category Score (10% weight)**
```
category_score = (common_categories / user_total_categories) × 100
```

### Filtering Options
- Minimum age
- Maximum age
- Minimum match percentage
- Pagination (page, page_size)

---

## Authentication Flow

1. **Registration**: User provides name, email, age, password → Password hashed with bcrypt → JWT token returned
2. **Login**: Email + password → Verify credentials → JWT token returned
3. **Protected Routes**: JWT token in Authorization header → Decoded and validated → User attached to request
4. **Token Refresh**: Valid token → New token issued

### JWT Configuration
- Algorithm: HS256
- Expiration: 24 hours (configurable)
- Payload: user_id, email, exp

---

## Frontend Pages

| Page | Route | Auth Required | Description |
|------|-------|---------------|-------------|
| Landing | `/` | ❌ | Hero section, features, CTA |
| Login | `/login` | Guest only | User authentication |
| Register | `/register` | Guest only | New user registration |
| Dashboard | `/dashboard` | ✅ | Profile, hobby selection |
| Matches | `/matches` | ✅ | Find & filter matches |

---

## UI Features

- **Dark Mode**: Toggle with persistence (localStorage)
- **Responsive Design**: Mobile-first approach
- **Animations**: Fade-in, slide-up, scale transitions
- **Toast Notifications**: Success, error, warning, info
- **Loading States**: Spinners and skeleton loaders
- **Form Validation**: Real-time validation feedback

---

## Environment Variables

### Backend (`.env`)
```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/hobby_matching_db
SECRET_KEY=your-secret-key-min-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=development
FRONTEND_URL=http://localhost:4200
```

### Frontend (`environment.ts`)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

---

## Deployment Strategy

### Backend (Render/Railway)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**: Set via platform dashboard

### Frontend (Vercel/Netlify)
- **Build Command**: `npm run build`
- **Output Directory**: `dist/hobby-matching-frontend/browser`
- **Environment**: Update `environment.prod.ts` with production API URL

---

## Pre-seeded Hobbies (50+)

The application automatically seeds hobbies in 7 categories:

| Category | Examples |
|----------|----------|
| Sports & Fitness | Soccer, Basketball, Yoga, Running |
| Arts & Creativity | Painting, Photography, Music Production |
| Technology | Programming, Gaming, Web Development |
| Entertainment | Movies, Reading, Board Games |
| Outdoor & Nature | Camping, Hiking, Traveling |
| Food & Culinary | Cooking, Baking, Coffee Brewing |
| Social & Community | Volunteering, Language Learning |

---

## Security Measures

- ✅ Password hashing (bcrypt)
- ✅ JWT authentication
- ✅ CORS configuration
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Rate limiting ready
- ✅ Environment-based secrets
