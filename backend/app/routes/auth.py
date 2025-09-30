from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models import User, UserFavorite
from app.auth import (
    create_access_token,
    get_current_active_user,
    get_user_info_from_google,
    create_or_get_user
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models
class SocialLoginRequest(BaseModel):
    access_token: str

class SocialLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    picture: Optional[str]
    provider: str
    created_at: datetime
    last_login: Optional[datetime]

class FavoriteRequest(BaseModel):
    stock_symbol: str

class FavoriteResponse(BaseModel):
    id: int
    stock_symbol: str
    created_at: datetime
    stock: dict

# Helper function to convert User to dict
def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "provider": user.provider,
        "created_at": user.created_at,
        "last_login": user.last_login
    }

# Google OAuth login
@router.post("/google", response_model=SocialLoginResponse)
async def google_login(
    request: SocialLoginRequest,
    db: Session = Depends(get_db)
):
    """Login with Google OAuth"""
    try:
        # Get user info from Google
        google_user = await get_user_info_from_google(request.access_token)
        
        # Create or get user
        user = create_or_get_user(
            db=db,
            provider="google",
            provider_id=google_user["id"],
            email=google_user["email"],
            name=google_user["name"],
            picture=google_user.get("picture")
        )
        
        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return SocialLoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_to_dict(user)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google login failed: {str(e)}"
        )


# Get current user info
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return UserResponse(**user_to_dict(current_user))

# Add stock to favorites
@router.post("/favorites", response_model=FavoriteResponse)
async def add_favorite(
    request: FavoriteRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a stock to user's favorites"""
    # Check if already favorited
    existing_favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.stock_symbol == request.stock_symbol
    ).first()
    
    if existing_favorite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock already in favorites"
        )
    
    # Create new favorite
    favorite = UserFavorite(
        user_id=current_user.id,
        stock_symbol=request.stock_symbol
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    # Get stock info
    from app.models import Stock
    stock = db.query(Stock).filter(Stock.symbol == request.stock_symbol).first()
    
    return FavoriteResponse(
        id=favorite.id,
        stock_symbol=favorite.stock_symbol,
        created_at=favorite.created_at,
        stock={
            "symbol": stock.symbol if stock else request.stock_symbol,
            "name": stock.name if stock else "Unknown",
            "price": stock.price if stock else None
        } if stock else {"symbol": request.stock_symbol, "name": "Unknown", "price": None}
    )

# Get user favorites
@router.get("/favorites")
async def get_favorites(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's favorite stocks"""
    favorites = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id
    ).all()
    
    result = []
    for favorite in favorites:
        from app.models import Stock
        stock = db.query(Stock).filter(Stock.symbol == favorite.stock_symbol).first()
        result.append({
            "id": favorite.id,
            "stock_symbol": favorite.stock_symbol,
            "created_at": favorite.created_at,
            "stock": {
                "symbol": stock.symbol if stock else favorite.stock_symbol,
                "name": stock.name if stock else "Unknown",
                "price": stock.price if stock else None,
                "balanced_score": stock.balanced_score if stock else None
            } if stock else {
                "symbol": favorite.stock_symbol,
                "name": "Unknown",
                "price": None,
                "balanced_score": None
            }
        })
    
    return result

# Remove stock from favorites
@router.delete("/favorites/{stock_symbol}")
async def remove_favorite(
    stock_symbol: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a stock from user's favorites"""
    favorite = db.query(UserFavorite).filter(
        UserFavorite.user_id == current_user.id,
        UserFavorite.stock_symbol == stock_symbol
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "Favorite removed successfully"}

# Logout (client-side token removal)
@router.post("/logout")
async def logout():
    """Logout endpoint (client should remove token)"""
    return {"message": "Logged out successfully"}
