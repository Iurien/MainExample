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