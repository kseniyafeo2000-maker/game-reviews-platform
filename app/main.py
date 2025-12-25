from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.database import engine, get_db
from app import models
from app.routers import games, reviews, users, auth

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameReviews Platform API",
    description="Платформа для обзоров видеоигр",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем маршруты
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(games.router, prefix="/api/games", tags=["games"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])

# Корневой маршрут
@app.get("/")
def read_root():
    return {
        "message": "Добро пожаловать в GameReviews Platform!",
        "api_docs": "/api/docs",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")