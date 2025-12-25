from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas
from app.database import get_db
from app.routers.users import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.GameResponse])
def read_games(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    games = crud.get_games(db, skip=skip, limit=limit, search=search)
    return games

@router.post("/", response_model=schemas.GameResponse)
def create_game(
    game: schemas.GameCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    return crud.create_game(db=db, game=game, user_id=current_user.id)

@router.get("/{game_id}", response_model=schemas.GameResponse)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = crud.get_game(db, game_id=game_id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.put("/{game_id}", response_model=schemas.GameResponse)
def update_game(
    game_id: int,
    game_update: schemas.GameBase,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    db_game = crud.update_game(db, game_id=game_id, game_update=game_update)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    success = crud.delete_game(db, game_id=game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game deleted successfully"}

@router.get("/{game_id}/reviews", response_model=List[schemas.ReviewResponse])
def read_game_reviews(
    game_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    reviews = crud.get_reviews(db, skip=skip, limit=limit, game_id=game_id)
    return reviews

@router.get("/{game_id}/stats")
def get_game_stats(game_id: int, db: Session = Depends(get_db)):
    stats = crud.get_game_statistics(db, game_id=game_id)
    return stats