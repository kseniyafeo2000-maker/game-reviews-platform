 🎮 GameReviews Platform

![Python](https://img.shields.io/badge/Python-3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)
![Render](https://img.shields.io/badge/Render.com-Cloud-purple)

Полнофункциональная платформа для обзоров видеоигр с современным FullStack стеком

🌐 Демо: [https://game-reviews-platform.onrender.com](https://game-reviews-platform-1.onrender.com/#)  
📚 API Документация: [https://game-reviews-platform.onrender.com/api/docs](https://game-reviews-platform.onrender.com/api/docs)  
🐙 GitHub: [https://github.com/kseniyafeo2000-maker/game-reviews-platform](https://github.com/kseniyafeo2000-maker/game-reviews-platform)

---

 📋 Содержание

1. [🚀 О проекте](-о-проекте)
2. [✨ Особенности](-особенности)
3. [🏗️ Архитектура](#️-архитектура)
4. [🛠️ Технологический стек](#️-технологический-стек)
5. [📁 Структура проекта](-структура-проекта)
6. [⚙️ Установка и запуск](#️-установка-и-запуск)
7. [📡 API Эндпоинты](-api-эндпоинты)
8. [🌐 Деплой на Render.com](-деплой-на-rendercom)
9. [📊 База данных](-база-данных)
10. [🎯 Для разработчиков](-для-разработчиков)
11. [📝 Лицензия](-лицензия)

---

 🚀 О проекте

GameReviews Platform - это полнофункциональное веб-приложение для публикации и чтения обзоров видеоигр. Проект разработан как учебный проект для демонстрации навыков FullStack разработки на Python.

 🎯 Основные цели проекта:
- ✅ Создание работающего облачного приложения
- ✅ Реализация полноценного REST API
- ✅ Интеграция с PostgreSQL базой данных
- ✅ Разработка адаптивного веб-интерфейса
- ✅ Деплой на бесплатном облачном хостинге

---

 ✨ Особенности

 🔧 Технические возможности:
- 🎯 CRUD операции - полный цикл создания, чтения, обновления и удаления
- 🗄️ Связанные таблицы - 4 таблицы с отношениями 1:N
- 🔐 Готовность к аутентификации - JWT и bcrypt в архитектуре
- 📱 Адаптивный дизайн - работает на всех устройствах
- ⚡ SPA архитектура - одностраничное приложение с динамической загрузкой

 🎨 Пользовательские возможности:
- 📝 Публикация обзоров на видеоигры
- ⭐ Система оценок от 1 до 10
- 🔍 Поиск и фильтрация игр
- 📊 Статистика по играм
- 💬 Комментарии к обзорам

---

 🏗️ Архитектура

 Схема базы данных:
```sql
users                    games
├── id (PK)             ├── id (PK)
├── username            ├── title
├── email               ├── description
├── hashed_password     ├── genre
└── created_at          ├── release_year
                        ├── developer
reviews                 └── created_at
├── id (PK)
├── game_id (FK → games.id)
├── user_id (FK → users.id)
├── content
├── rating (1-10)
└── created_at
```

 Архитектурная схема:
```
┌─────────────────────────────────────────────────────┐
│                Пользовательский интерфейс           │
│  • Одностраничное приложение (SPA)                  │
│  • HTML5 / CSS3 / JavaScript                        │
│  • Адаптивный дизайн                                │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│                REST API (FastAPI)                   │
│  • /api/games - управление играми                   │
│  • /api/reviews - управление обзорами               │
│  • /api/users - управление пользователями           │
│  • Автоматическая документация Swagger/OpenAPI      │
└──────────────────────────┬──────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────┐
│                База данных (PostgreSQL)             │
│  • 4 нормализованные таблицы                        │
│  • Связи 1:N между сущностями                       │
│  • Индексы для оптимизации запросов                 │
└─────────────────────────────────────────────────────┘
```

---

 🛠️ Технологический стек

 Backend:
- Python 3.9 - основной язык программирования
- FastAPI 0.68.0 - современный асинхронный фреймворк
- SQLAlchemy 1.4 - ORM для работы с базой данных
- Pydantic 1.10 - валидация данных и сериализация
- PostgreSQL - реляционная база данных
- Uvicorn - ASGI сервер для запуска приложения

 Frontend:
- HTML5 - семантическая разметка
- CSS3 - Flexbox, Grid, анимации
- JavaScript (ES6+) - Vanilla JS без фреймворков
- Fetch API - взаимодействие с бэкендом

 DevOps:
- Render.com - облачный хостинг и база данных
- Git/GitHub - контроль версий
- Docker - контейнеризация (готовность)

---

 📁 Структура проекта

```
game-reviews-platform/
├── app/                     Основное приложение
│   ├── __init__.py
│   ├── main.py             Точка входа приложения
│   ├── database.py         Настройка подключения к БД
│   ├── models.py           SQLAlchemy модели данных
│   ├── schemas.py          Pydantic схемы валидации
│   ├── crud.py             CRUD операции с БД
│   └── routers/            Маршруты API
│       ├── __init__.py
│       └── games.py        API для управления играми
├── static/                 Статические файлы
│   ├── css/
│   │   └── style.css       Стили приложения
│   └── js/
│       └── main.js         Клиентский JavaScript
├── templates/              HTML шаблоны
│   └── index.html          Главная страница SPA
├── requirements.txt        Зависимости Python
├── runtime.txt            Версия Python для Render
├── render.yaml            Конфигурация для Render.com
├── .gitignore             Игнорируемые файлы Git
└── README.md              Эта документация
```

---

 ⚙️ Установка и запуск

 Локальная разработка:

 1. Клонирование репозитория:
```bash
git clone https://github.com/kseniyafeo2000-maker/game-reviews-platform.git
cd game-reviews-platform
```

 2. Создание виртуального окружения:
```bash
python -m venv venv

 Активация на Windows:
venv\Scripts\activate

 Активация на Mac/Linux:
source venv/bin/activate
```

 3. Установка зависимостей:
```bash
pip install -r requirements.txt
```

 4. Настройка базы данных:
```bash
 Вариант A: Docker (рекомендуется)
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

 Вариант B: Установка PostgreSQL локально
 Скачайте с https://www.postgresql.org/download/
```

 5. Настройка переменных окружения:
Создайте файл `.env` в корне проекта:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/game_reviews
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

 6. Запуск приложения:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

 7. Откройте в браузере:
- 🌐 Приложение: http://localhost:8000
- 📚 API Документация: http://localhost:8000/api/docs

---

 📡 API Эндпоинты

 Игры (Games)
| Метод | Эндпоинт | Описание | Аутентификация |
|-------|----------|----------|----------------|
| `GET` | `/api/games` | Получить список всех игр | ❌ Не требуется |
| `POST` | `/api/games` | Создать новую игру | ❌ Не требуется |
| `GET` | `/api/games/{id}` | Получить информацию об игре | ❌ Не требуется |
| `PUT` | `/api/games/{id}` | Обновить информацию об игре | ❌ Не требуется |
| `DELETE` | `/api/games/{id}` | Удалить игру | ❌ Не требуется |

 Примеры запросов:

 Создание игры:
```bash
curl -X POST "http://localhost:8000/api/games" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Legend of Zelda: Breath of the Wild",
    "genre": "Action-Adventure",
    "release_year": 2017,
    "developer": "Nintendo",
    "description": "Открытый мир приключений в Хайруле"
  }'
```

 Получение списка игр:
```bash
curl "http://localhost:8000/api/games"
```

 Обновление игры:
```bash
curl -X PUT "http://localhost:8000/api/games/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Обновленное название",
    "genre": "RPG"
  }'
```

---

 🌐 Деплой на Render.com

 1. Подготовка репозитория:
- Загрузите код на GitHub
- Убедитесь что есть файлы:
  - ✅ `requirements.txt`
  - ✅ `runtime.txt` (python-3.9.0)
  - ✅ `app/main.py`

 2. Создание базы данных на Render:
1. Откройте [Render Dashboard](https://render.com/dashboard)
2. New+ → PostgreSQL
3. Настройки:
   - Name: `game-reviews-db`
   - Database: `game_reviews`
   - Plan: Free
4. Нажмите Create Database
5. Скопируйте External Database URL

 3. Создание Web Service:
1. New+ → Web Service
2. Подключите ваш GitHub репозиторий
3. Настройки:
   - Name: `game-reviews-platform`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free
4. Добавьте Environment Variables:
   - `DATABASE_URL`: (вставьте скопированный URL)
   - `SECRET_KEY`: `your-production-secret-key`
   - `DEBUG`: `false`
5. Нажмите Create Web Service

 4. Деплой автоматически запустится:
- Ждите 5-10 минут
- Проверьте логи во вкладке Logs
- При успешном деплое получите URL вида: `https://game-reviews-platform.onrender.com`

---

 📊 База данных

 Миграции и управление:
Для создания таблиц при запуске используется SQLAlchemy:
```python
 app/main.py
models.Base.metadata.create_all(bind=engine)
```

 Работа с данными:
```python
 Пример использования CRUD операций
from app.database import SessionLocal
from app import crud, schemas

db = SessionLocal()

 Создание игры
new_game = schemas.GameCreate(
    title="Elden Ring",
    genre="Action RPG",
    release_year=2022,
    developer="FromSoftware"
)
created_game = crud.create_game(db, new_game)

 Получение списка игр
games = crud.get_games(db, skip=0, limit=10)
```

 Демо-данные:
При первом запуске база данных пуста. Для тестирования используйте:
1. Форму на главной странице
2. API через Swagger документацию
3. Команды curl из терминала

---

 🎯 Для разработчиков

 Разработка новой функциональности:

 1. Добавление новой сущности:
```python
 1. Добавьте модель в app/models.py
 2. Создайте схемы в app/schemas.py
 3. Реализуйте CRUD операции в app/crud.py
 4. Создайте роутер в app/routers/
 5. Подключите роутер в app/main.py
```

 2. Тестирование:
```bash
 Запуск тестов (требуется настройка pytest)
pytest tests/

 Тестирование API через curl
curl -X POST "https://your-app.onrender.com/api/games" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Game", "genre": "Test"}'
```

 3. Отладка:
- Проверяйте логи на Render.com
- Используйте Swagger UI для тестирования API
- Включите `DEBUG=True` для детальных сообщений об ошибках

 Git workflow:
```bash
 Создание новой ветки
git checkout -b feature/new-feature

 Коммит изменений
git add .
git commit -m "Описание изменений"

 Отправка в репозиторий
git push origin feature/new-feature

 Создание Pull Request на GitHub
```

---

 📝 Лицензия

Этот проект разработан для образовательных целей. Все права на использованные материалы принадлежат их авторам.

 Благодарности:
- FastAPI сообществу за отличную документацию
- Render.com за бесплатный хостинг для студентов
- SQLAlchemy за мощный и гибкий ORM

---

 📞 Поддержка

 Полезные ссылки:
- 📚 [FastAPI документация](https://fastapi.tiangolo.com)
- 🗄️ [SQLAlchemy документация](https://docs.sqlalchemy.org)
- 🌐 [Render.com документация](https://render.com/docs)
- 🐙 [GitHub репозиторий](https://github.com/kseniyafeo2000-maker/game-reviews-platform)

 Если возникли проблемы:
1. Проверьте логи на Render.com
2. Убедитесь что все Environment Variables настроены
3. Проверьте подключение к базе данных
4. Создайте issue в GitHub репозитории

---

🎓 Учебный проект разработан для демонстрации навыков FullStack разработки

✨ Удачи в изучении программирования!
