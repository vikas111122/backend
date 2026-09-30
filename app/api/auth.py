from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt
from app.config import settings
from app.schemas.auth import LoginRequest, TokenResponse
from app.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])

def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/login", response_model=TokenResponse)
def user_login(credentials: LoginRequest):
    if credentials.username == "operator" and credentials.password == "password123":
        token = create_jwt_token({"sub": credentials.username, "role": "user"})
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_role="user",
            username=credentials.username
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

@router.post("/admin/login", response_model=TokenResponse)
def admin_login(credentials: LoginRequest):
    if credentials.username == "admin" and credentials.password == "admin123":
        token = create_jwt_token({"sub": credentials.username, "role": "admin"})
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user_role="admin",
            username=credentials.username
        )
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid admin credentials")

@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user)):
    return {"message": "Token is valid!", "user": current_user}

@router.get("/admin/test")
def test_admin_access(admin_user: dict = Depends(require_admin)):
    return {"message": "Welcome Admin!", "user": admin_user}