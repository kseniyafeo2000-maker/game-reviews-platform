// Базовый API клиент
const API_BASE_URL = window.location.origin + '/api';
let currentToken = localStorage.getItem('token');

const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (currentToken) {
            headers['Authorization'] = `Bearer ${currentToken}`;
        }

        const response = await fetch(url, {
            ...options,
            headers
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            currentToken = null;
            showLogin();
            throw new Error('Session expired');
        }

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }

        return response.json();
    },

    async getGames(search = '') {
        const query = search ? `?search=${encodeURIComponent(search)}` : '';
        return this.request(`/games${query}`);
    },

    async getGame(id) {
        return this.request(`/games/${id}`);
    },

    async createGame(game) {
        return this.request('/games', {
            method: 'POST',
            body: JSON.stringify(game)
        });
    },

    async getGameReviews(gameId) {
        return this.request(`/games/${gameId}/reviews`);
    },

    async createReview(review) {
        return this.request('/reviews', {
            method: 'POST',
            body: JSON.stringify(review)
        });
    },

    async register(user) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(user)
        });
    },

    async login(email, password) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        currentToken = data.access_token;
        localStorage.setItem('token', currentToken);
        return data;
    },

    async getCurrentUser() {
        try {
            return await this.request('/users/me');
        } catch (error) {
            return null;
        }
    }
};

// Утилиты
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => alertDiv.remove(), 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Рендеринг
function renderGameCard(game) {
    return `
        <div class="card game-card">
            <h3>${game.title}</h3>
            ${game.genre ? `<p><strong>Жанр:</strong> ${game.genre}</p>` : ''}
            ${game.release_year ? `<p><strong>Год выпуска:</strong> ${game.release_year}</p>` : ''}
            ${game.developer ? `<p><strong>Разработчик:</strong> ${game.developer}</p>` : ''}
            ${game.description ? `<p>${game.description.substring(0, 100)}...</p>` : ''}
            <button onclick="viewGame(${game.id})" class="btn">Подробнее</button>
        </div>
    `;
}

function renderReviewCard(review) {
    const stars = '★'.repeat(review.rating) + '☆'.repeat(10 - review.rating);
    return `
        <div class="card review-card">
            <div class="rating">${stars} (${review.rating}/10)</div>
            <p>${review.content}</p>
            <small>Автор: ${review.author.username} • ${formatDate(review.created_at)}</small>
        </div>
    `;
}

// Навигация
function showHome() {
    document.getElementById('content').innerHTML = `
        <div class="main-content">
            <h2>Последние игры</h2>
            <div class="form-group">
                <input type="text" id="searchInput" placeholder="Поиск игр..." 
                       oninput="searchGames()">
            </div>
            <div id="gamesList"></div>
            ${currentToken ? `
                <button onclick="showAddGame()" class="btn btn-success">Добавить игру</button>
            ` : ''}
        </div>
    `;
    loadGames();
}

async function loadGames(search = '') {
    try {
        const games = await api.getGames(search);
        const gamesList = document.getElementById('gamesList');
        gamesList.innerHTML = games.map(renderGameCard).join('');
    } catch (error) {
        showAlert(error.message, 'error');
    }
}

function searchGames() {
    const search = document.getElementById('searchInput').value;
    loadGames(search);
}

// Инициализация
document.addEventListener('DOMContentLoaded', async () => {
    const user = await api.getCurrentUser();
    if (user) {
        document.getElementById('userInfo').textContent = user.username;
        document.getElementById('authButtons').innerHTML = `
            <button onclick="logout()" class="btn">Выйти</button>
        `;
    }
    showHome();
});

function logout() {
    localStorage.removeItem('token');
    currentToken = null;
    location.reload();
}