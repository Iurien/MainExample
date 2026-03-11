document.addEventListener('DOMContentLoaded', () => {
    // 1. Эффект печатной машинки
    const textElement = document.getElementById('typewriter');
    const phrases = [
        'Господа Иисуса Христа',
        'Пострадавшего за нас на кресте',
        'Принявшего все грехи наши на себя'
    ];
    const colors = ['#FFD700', '#FF4500', '#87CEEB'];
    let i = 0, j = 0, isDeleting = false;

    function type() {
        if (!textElement) return; // Защита, если элемента нет

        const current = phrases[i];
        textElement.style.color = colors[i];

        textElement.textContent = isDeleting
            ? current.substring(0, j--)
            : current.substring(0, j++);

        if (!isDeleting && j === current.length + 1) {
            isDeleting = true;
            setTimeout(type, 1500);
        } else if (isDeleting && j === 0) {
            isDeleting = false;
            i = (i + 1) % phrases.length;
            setTimeout(type, 500);
        } else {
            setTimeout(type, isDeleting ? 50 : 150);
        }
    }

    if (textElement) type();

    // 2. Переключение темы
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const body = document.body;
            const newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // 3. Модальное окно
    const modal = document.getElementById('modal-project');
    const openBtns = document.querySelectorAll('.open-modal');
    const closeBtn = document.querySelector('.modal__close');

    if (modal) {
        openBtns.forEach(btn => {
            btn.onclick = () => modal.classList.add('modal--active');
        });

        if (closeBtn) {
            closeBtn.onclick = () => modal.classList.remove('modal--active');
        }

        window.addEventListener('click', (e) => {
            const overlay = modal.querySelector('.modal__overlay');
            if (e.target === overlay || e.target === modal) {
                modal.classList.remove('modal--active');
            }
        });
    }

    // 4. Reveal Animation (Intersection Observer)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal--active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // 5. индикатор загрузки
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        // Используем load, чтобы скрыть после полной загрузки всех картинок
        window.addEventListener('load', () => {
            preloader.style.display = 'none';
        });
        // Резервное скрытие, если load не сработал быстро
        setTimeout(() => { preloader.style.display = 'none'; }, 3000);
    }

    // 6. Авто-скрытие сообщений
    setTimeout(() => {
        const msg = document.querySelector('.messages');
        if (msg) msg.style.opacity = '0'; // Плавнее через opacity
        setTimeout(() => { if(msg) msg.style.display = 'none'; }, 500);
    }, 5000);
});