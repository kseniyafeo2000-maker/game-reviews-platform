from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app import models, schemas
from app.auth import get_password_hash, verify_password
from datetime import datetime

# ========== USER CRUD ==========
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# ========== GAME CRUD ==========
def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_games(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Game)
    if search:
        query = query.filter(
            or_(
                models.Game.title.ilike(f"%{search}%"),
                models.Game.genre.ilike(f"%{search}%"),
                models.Game.developer.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_game(db: Session, game: schemas.GameCreate, user_id: int):
    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def update_game(db: Session, game_id: int, game_update: schemas.GameBase):
    db_game = get_game(db, game_id)
    if not db_game:
        return None
    
    update_data = game_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_game, field, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game

def delete_game(db: Session, game_id: int):
    db_game = get_game(db, game_id)
    if db_game:
        db.delete(db_game)
        db.commit()
        return True
    return False

# ========== REVIEW CRUD ==========
def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_reviews(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    game_id: Optional[int] = None,
    user_id: Optional[int] = None
):
    query = db.query(models.Review)
    if game_id:
        query = query.filter(models.Review.game_id == game_id)
    if user_id:
        query = query.filter(models.Review.user_id == user_id)
    
    return query.offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    db_review = models.Review(
        **review.model_dump(),
        user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_update: schemas.ReviewBase, user_id: int):
    db_review = get_review(db, review_id)
    if not db_review or db_review.user_id != user_id:
        return None
    
    update_data = review_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_review, field, value)
    
    db.commit()
    db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int, user_id: int):
    db_review = get_review(db, review_id)
    if db_review and db_review.user_id == user_id:
        db.delete(db_review)
        db.commit()
        return True
    return False

# ========== COMMENT CRUD ==========
def get_comments_by_review(db: Session, review_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).filter(
        models.Comment.review_id == review_id
    ).offset(skip).limit(limit).all()

def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int):
    db_comment = models.Comment(
        **comment.model_dump(),
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    db_comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.user_id == user_id
    ).first()
    
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return True
    return False

# ========== STATISTICS ==========
def get_game_statistics(db: Session, game_id: int):
    reviews = db.query(models.Review).filter(models.Review.game_id == game_id).all()
    if not reviews:
        return {"average_rating": 0, "total_reviews": 0}
    
    total_rating = sum(review.rating for review in reviews)
    average_rating = total_rating / len(reviews)
    
    return {
        "average_rating": round(average_rating, 2),
        "total_reviews": len(reviews)
    }