from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.ReviewResponse])
def read_reviews(
    skip: int = 0,
    limit: int = 100,
    game_id: int = None,
    db: Session = Depends(get_db)
):
    reviews = crud.get_reviews(db, skip=skip, limit=limit, game_id=game_id)
    return reviews

@router.post("/", response_model=schemas.ReviewResponse)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    # Проверяем, существует ли игра
    game = crud.get_game(db, game_id=review.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return crud.create_review(db=db, review=review, user_id=current_user.id)

@router.get("/{review_id}", response_model=schemas.ReviewResponse)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.put("/{review_id}", response_model=schemas.ReviewResponse)
def update_review(
    review_id: int,
    review_update: schemas.ReviewBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    db_review = crud.update_review(
        db, review_id=review_id, review_update=review_update, user_id=current_user.id
    )
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found or access denied")
    return db_review

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    success = crud.delete_review(db, review_id=review_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found or access denied")
    return {"message": "Review deleted successfully"}

@router.get("/{review_id}/comments", response_model=List[schemas.CommentResponse])
def read_review_comments(
    review_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    comments = crud.get_comments_by_review(db, review_id=review_id, skip=skip, limit=limit)
    return comments

@router.post("/{review_id}/comments", response_model=schemas.CommentResponse)
def create_comment(
    review_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    # Проверяем, существует ли обзор
    review = crud.get_review(db, review_id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    comment_data = comment.model_dump()
    comment_data["review_id"] = review_id
    
    return crud.create_comment(
        db=db, 
        comment=schemas.CommentCreate(**comment_data),
        user_id=current_user.id
    )