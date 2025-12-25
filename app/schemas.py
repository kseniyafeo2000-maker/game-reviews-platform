from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Game schemas
class GameBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1970, le=2024)
    developer: Optional[str] = None

class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Review schemas
class ReviewBase(BaseModel):
    content: str = Field(..., min_length=10)
    rating: int = Field(..., ge=1, le=10)

class ReviewCreate(ReviewBase):
    game_id: int

class ReviewResponse(ReviewBase):
    id: int
    game_id: int
    user_id: int
    author: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# Comment schemas
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    review_id: int

class CommentResponse(CommentBase):
    id: int
    review_id: int
    user_id: int
    author: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None