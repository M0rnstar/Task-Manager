document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
        // Убираем активный класс со всех элементов
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));

        // Добавляем активный класс текущему элементу
        this.classList.add('active');
    });
});

// Находим кнопку
const addTask = document.getElementById('addTask');

// Находим контейнер с карточками
const cardsContainer = document.querySelector('.cards');

// Добавляем обработчик события клика по кнопке
addTask.addEventListener('click', function() {
    // Создаём новую карточку с нужной структурой
    const newCard = document.createElement('div');
    newCard.classList.add('card');
    newCard.innerHTML = `
        <div class="card__content">
            <div class="card__left">
                <input type="checkbox" class="checkbox" />
            </div>
            <div class="card__right">
                <div class="card__deadline">До 31 мая</div>
                <div class="card__title">Новая задача</div>
            </div>
        </div>
    `;

    // Добавляем новую карточку в контейнер
    cardsContainer.appendChild(newCard);
});

// Получаем элементы
const username = document.getElementById('username');
const dropdownMenu = document.getElementById('dropdownMenu');

// Открываем/закрываем шторку при клике на никнейм
username.addEventListener('click', function() {
    // Переключаем display между 'none' и 'block'
    if (dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '') {
        dropdownMenu.style.display = 'block';
    } else {
        dropdownMenu.style.display = 'none';
    }
});

// Закрываем шторку, если клик был вне меню
window.addEventListener('click', function(event) {
    if (!event.target.closest('#username') && !event.target.closest('#dropdownMenu')) {
        dropdownMenu.style.display = 'none';
    }
});