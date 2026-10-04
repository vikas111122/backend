
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.utils.security import verify_password, get_password_hash
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Seed Endpoint: Run once to seed initial operator & admin users into SQL Server
@router.post("/seed-users")
def seed_users(db: Session = Depends(get_db)):
    if not db.query(User).filter(User.username == "operator").first():
        user = User(username="operator", hashed_password=get_password_hash("password123"), role="user")
        db.add(user)
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(username="admin", hashed_password=get_password_hash("admin123"), role="admin")
        db.add(admin)
    db.commit()
    return {"message": "Users seeded into MS SQL Server successfully"}

# Database-backed Login Endpoint
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )

    token = create_jwt_token({"sub": user.username, "role": user.role})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user_role=user.role,
        username=user.username
    )

@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"message": "Token is valid!", "user": current_user}

@router.get("/admin/test")
def test_admin_access(admin_user: dict = Depends(require_admin)):
    return {"message": "Welcome Admin!", "user": admin_user}
