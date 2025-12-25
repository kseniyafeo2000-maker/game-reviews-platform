// Функции для навигации
async function showHome() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section">
            <h2><i class="fas fa-home"></i> Добро пожаловать на GameReviews Platform!</h2>
            <p>Здесь вы можете читать и писать обзоры на видеоигры.</p>
            <p>Используйте меню для навигации по платформе.</p>
            <div class="stats">
                <div class="stat-card">
                    <h3><i class="fas fa-gamepad"></i> Игр в базе</h3>
                    <p id="gamesCount">Загрузка...</p>
                </div>
                <div class="stat-card">
                    <h3><i class="fas fa-users"></i> Пользователей</h3>
                    <p id="usersCount">Загрузка...</p>
                </div>
            </div>
        </div>
    `;
    await loadStats();
}

async function showGames() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section">
            <h2><i class="fas fa-list"></i> Все игры</h2>
            <div id="gamesList">Загрузка игр...</div>
        </div>
    `;
    await loadGames();
}

function showReviews() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section">
            <h2><i class="fas fa-star"></i> Обзоры</h2>
            <p>Здесь будут отображаться обзоры игр.</p>
            <p>Функция находится в разработке.</p>
        </div>
    `;
}

function showLogin() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section">
            <h2><i class="fas fa-sign-in-alt"></i> Вход в систему</h2>
            <form onsubmit="handleLogin(event)">
                <input type="text" id="loginUsername" placeholder="Имя пользователя" required>
                <input type="password" id="loginPassword" placeholder="Пароль" required>
                <button type="submit" class="btn btn-success">Войти</button>
            </form>
        </div>
    `;
}

function showRegister() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="section">
            <h2><i class="fas fa-user-plus"></i> Регистрация</h2>
            <form onsubmit="handleRegister(event)">
                <input type="text" id="regUsername" placeholder="Имя пользователя" required>
                <input type="email" id="regEmail" placeholder="Email" required>
                <input type="password" id="regPassword" placeholder="Пароль" required>
                <button type="submit" class="btn btn-success">Зарегистрироваться</button>
            </form>
        </div>
    `;
}

// Загрузка данных с API
async function loadStats() {
    try {
        const gamesResponse = await fetch('/api/games');
        const usersResponse = await fetch('/api/users');
        
        const games = await gamesResponse.json();
        const users = await usersResponse.json();
        
        document.getElementById('gamesCount').textContent = games.length;
        document.getElementById('usersCount').textContent = users.length;
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
        document.getElementById('gamesCount').textContent = 'Ошибка';
        document.getElementById('usersCount').textContent = 'Ошибка';
    }
}

async function loadGames() {
    try {
        const response = await fetch('/api/games');
        const games = await response.json();
        
        let html = '<div class="games-grid">';
        games.forEach(game => {
            html += `
                <div class="game-card">
                    <h3>${game.title}</h3>
                    <p>${game.description || 'Нет описания'}</p>
                    <p><small>ID: ${game.id}</small></p>
                </div>
            `;
        });
        html += '</div>';
        
        document.getElementById('gamesList').innerHTML = html;
    } catch (error) {
        console.error('Ошибка загрузки игр:', error);
        document.getElementById('gamesList').innerHTML = '<p class="error">Ошибка загрузки игр</p>';
    }
}

// Обработчики форм
function handleLogin(event) {
    event.preventDefault();
    alert('Функция входа в разработке');
}

function handleRegister(event) {
    event.preventDefault();
    alert('Функция регистрации в разработке');
}

// Проверка авторизации (заглушка)
function checkAuth() {
    const token = localStorage.getItem('token');
    const authButtons = document.getElementById('authButtons');
    const userInfo = document.getElementById('userInfo');
    
    if (token) {
        authButtons.style.display = 'none';
        userInfo.innerHTML = `
            <span><i class="fas fa-user"></i> Пользователь</span>
            <button onclick="logout()" class="btn btn-danger" style="margin-left: 10px;">
                <i class="fas fa-sign-out-alt"></i> Выйти
            </button>
        `;
    }
}

function logout() {
    localStorage.removeItem('token');
    location.reload();
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Показываем главную страницу по умолчанию
    showHome();
    
    // Проверяем авторизацию
    checkAuth();
});
