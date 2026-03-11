document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('#sidebar-wrapper');
    const sidebarLinks = document.querySelectorAll('.sidebar-nav-item a');

    // Открыть/закрыть по клику на гамбургер
    menuToggle.addEventListener('click', function(e) {
        e.preventDefault();
        sidebar.classList.toggle('active');
        this.classList.toggle('active');
    });

    // Закрыть при клике на любой пункт меню
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            sidebar.classList.remove('active');
            menuToggle.classList.remove('active');
        });
    });
});

