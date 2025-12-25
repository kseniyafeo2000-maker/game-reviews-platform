from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os

# Получаем абсолютный путь к корневой директории
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="GameReviews Platform API")

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы - ТОЛЬКО ОДИН РАЗ с правильным путем
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Пример модели данных
class Game(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

# Демо данные
demo_games = [
    {"id": 1, "title": "The Witcher 3", "description": "RPG игра"},
    {"id": 2, "title": "Cyberpunk 2077", "description": "Футуристический экшен"},
]

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/api/games", response_model=List[Game])
async def get_games():
    return demo_games

@app.get("/api/users")
async def get_users():
    return [{"id": 1, "username": "test_user"}]

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
