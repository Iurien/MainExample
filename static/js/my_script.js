const btn = document.getElementById('theme-toggle');
const html = document.documentElement;

// Проверяем сохраненную тему при загрузке
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-bs-theme', savedTheme);
updateBtnText(savedTheme);

btn.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateBtnText(newTheme);
});

function updateBtnText(theme) {
    btn.innerHTML = theme === 'light' ? 'Сменить тему 🌙' : 'Сменить тему ☀️';
}


// Библиотека AOS
AOS.init({
    duration: 800, // Скорость анимации (мс)
    once: true,    // Анимация срабатывает только один раз при скролле
    offset: 50     // Запуск анимации чуть раньше появления элемента
});


// Иконки боковой панели
document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.dzen-nav-link');

    links.forEach(link => {
      link.addEventListener('click', function(e) {
        // Удаляем активный класс у всех
        links.forEach(l => {
          l.classList.remove('active');
          l.setAttribute('aria-selected', 'false');
        });

        // Добавляем текущему
        this.classList.add('active');
        this.setAttribute('aria-selected', 'true');
      });
    });
  });

// Боковое меню образец
// Переключение меню по клику на кнопку (её нужно добавить в HTML)
const menuToggle = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('#sidebar-wrapper');

menuToggle.addEventListener('click', (e) => {
    e.preventDefault();
    sidebar.classList.toggle('active');
});

// Закрытие при клике на пункт меню
document.querySelectorAll('.sidebar-nav-item a').forEach(link => {
    link.addEventListener('click', () => {
        sidebar.classList.remove('active');
    });
});


// Кнопка вверх/вниз
const scrollNav = document.getElementById('scrollNav');
const btnUp = document.getElementById('goUp');
const btnDown = document.getElementById('goDown');

// Показываем кнопки, если прокрутили больше 300px
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollNav.classList.add('scroll-nav--visible');
    } else {
        scrollNav.classList.remove('scroll-nav--visible');
    }
});

// Плавный скролл вверх
btnUp.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Плавный скролл вниз
btnDown.addEventListener('click', () => {
    window.scrollTo({
        top: document.documentElement.scrollHeight,
        behavior: 'smooth'
    });
});
