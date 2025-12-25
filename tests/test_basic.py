import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем тестовые таблицы
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_login_user():
    login_data = {
        "username": "test@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_games():
    response = client.get("/api/games")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_game_without_auth():
    game_data = {
        "title": "Test Game",
        "genre": "RPG",
        "release_year": 2023
    }
    response = client.post("/api/games", json=game_data)
    assert response.status_code == 401  # Unauthorized

@pytest.fixture
def auth_headers():
    # Регистрируем и логиним пользователя
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123"
    }
    client.post("/api/auth/register", json=user_data)
    
    login_data = {
        "username": "test2@example.com",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

def test_create_game_with_auth(auth_headers):
    game_data = {
        "title": "Auth Test Game",
        "genre": "Strategy",
        "release_year": 2024
    }
    response = client.post(
        "/api/games", 
        json=game_data, 
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == game_data["title"]
    assert data["genre"] == game_data["genre"]