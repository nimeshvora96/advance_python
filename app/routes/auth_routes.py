from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse, Token
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBasic()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return AuthController.register_user(user_data, db)

@router.post("/login", response_model=Token)
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """Login user and get access token"""
    return AuthController.login_user(credentials.username, credentials.password, db)