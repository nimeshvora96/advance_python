## 1️ Setup Instructions

# Steps
1. Clone the repository
   git clone (https://github.com/nimeshvora96/advance_python)

2. Create a virtual environment & activate it
   python -m venv .venv
   .\.venv\Scripts\activate   # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Create `.env` file

5. Run database migrations
   alembic upgrade head
   
## 2 How to Run the App

uvicorn app.main:app --reload
➡ http://localhost:8000

## 3️ API Testing Guide
# Using Postman
1. Import the API:  
   **http://localhost:8000/endpoint**
2. Set `Authorization` → `Bearer Token` with the JWT you receive from `/auth/login`
3. Test endpoints for Students, Teachers, and Enrollments

## 4️ Environment Variables (`.env`)
# Database
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name

# JWT Auth
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

## 5️ Redis Configuration / Setup

# Install Redis

redis-cli ping
# Expected output: PONG
