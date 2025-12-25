import uvicorn  # Импорт должен быть в начале файла
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

# Проверяем существование папок (для отладки)
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

print(f"Base directory: {BASE_DIR}")
print(f"Static directory: {STATIC_DIR} - exists: {os.path.exists(STATIC_DIR)}")
print(f"Templates directory: {TEMPLATES_DIR} - exists: {os.path.exists(TEMPLATES_DIR)}")

# Если папок нет, создаем их (опционально, для безопасности)
if not os.path.exists(STATIC_DIR):
    print(f"WARNING: Static directory not found: {STATIC_DIR}")
if not os.path.exists(TEMPLATES_DIR):
    print(f"WARNING: Templates directory not found: {TEMPLATES_DIR}")

app = FastAPI(title="GameReviews Platform API")

# Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Пример модели данных
class Game(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

# Демо данные
demo_games = [
    {"id": 1, "title": "The Witcher 3", "description": "RPG игра"},
    {"id": 2, "title": "Cyberpunk 2077", "description": "Футуристический экшен"},
    {"id": 3, "title": "Elden Ring", "description": "Открытый мир, Dark Souls стиль"},
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

@app.get("/api/health")
async def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "ok", 
        "service": "GameReviews Platform API",
        "version": "1.0.0"
    }

@app.get("/api/docs")
async def get_api_docs_redirect():
    """Перенаправление на Swagger документацию"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

# Для запуска в режиме разработки
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
