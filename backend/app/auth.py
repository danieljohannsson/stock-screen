import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Password context (for future use if needed)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Social login utilities
async def get_user_info_from_google(access_token: str) -> dict:
    """Get user info from Google using access token"""
    import httpx
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not get user info from Google"
            )


def create_or_get_user(db: Session, provider: str, provider_id: str, email: str, name: str, picture: str = None) -> User:
    """Create or get existing user from social login"""
    # Try to find existing user by provider and provider_id
    user = db.query(User).filter(
        User.provider == provider,
        User.provider_id == provider_id
    ).first()
    
    if user:
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    # Try to find user by email (in case they used different provider)
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        # Update existing user with new provider info
        existing_user.provider = provider
        existing_user.provider_id = provider_id
        existing_user.last_login = datetime.utcnow()
        if picture and not existing_user.picture:
            existing_user.picture = picture
        db.commit()
        db.refresh(existing_user)
        return existing_user
    
    # Create new user
    new_user = User(
        email=email,
        name=name,
        picture=picture,
        provider=provider,
        provider_id=provider_id,
        last_login=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
