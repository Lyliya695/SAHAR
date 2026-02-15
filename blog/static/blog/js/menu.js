// blog/js/menu.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, инициализация меню...');
    
    const burgerMenu = document.querySelector('.burger-menu');
    const mobileMenu = document.querySelector('.mobile-menu');
    const overlay = document.querySelector('.overlay');
    const closeMenuBtn = document.querySelector('.close-menu');
    
    console.log('Найдены элементы:', {
        burgerMenu,
        mobileMenu,
        overlay,
        closeMenuBtn
    });
    
    if (!burgerMenu) {
        console.error('Не найден .burger-menu');
        return;
    }
    
    if (!mobileMenu) {
        console.error('Не найден .mobile-menu');
        return;
    }
    
    if (!overlay) {
        console.error('Не найден .overlay');
        return;
    }
    
    if (!closeMenuBtn) {
        console.error('Не найден .close-menu');
        return;
    }
    
    // Открытие/закрытие меню по клику на бургер
    burgerMenu.addEventListener('click', function(e) {
        console.log('Клик по бургеру');
        e.stopPropagation();
        toggleMenu();
    });
    
    // Закрытие меню по клику на крестик
    closeMenuBtn.addEventListener('click', function(e) {
        console.log('Клик по крестику');
        e.stopPropagation();
        closeMenu();
    });
    
    // Закрытие меню по клику на оверлей
    overlay.addEventListener('click', function(e) {
        console.log('Клик по оверлею');
        e.stopPropagation();
        closeMenu();
    });
    
    // Закрытие меню по клику на ссылку в мобильном меню
    const mobileMenuLinks = mobileMenu.querySelectorAll('a');
    mobileMenuLinks.forEach(link => {
        link.addEventListener('click', function() {
            console.log('Клик по ссылке в меню');
            closeMenu();
        });
    });
    
    // Закрытие меню по клику на кнопку выхода в мобильном меню
    const mobileLogoutBtn = mobileMenu.querySelector('button[type="submit"]');
    if (mobileLogoutBtn) {
        mobileLogoutBtn.addEventListener('click', function() {
            console.log('Клик по кнопке выхода');
            setTimeout(closeMenu, 100);
        });
    }
    
    // Закрытие меню по клавише ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileMenu.classList.contains('active')) {
            console.log('Нажата клавиша ESC');
            closeMenu();
        }
    });
    
    function toggleMenu() {
        console.log('toggleMenu вызван');
        console.log('Состояние до:', {
            burgerMenuOpen: burgerMenu.classList.contains('open'),
            mobileMenuActive: mobileMenu.classList.contains('active'),
            overlayActive: overlay.classList.contains('active')
        });
        
        burgerMenu.classList.toggle('open');
        mobileMenu.classList.toggle('active');
        overlay.classList.toggle('active');
        
        const isMenuOpen = mobileMenu.classList.contains('active');
        document.body.style.overflow = isMenuOpen ? 'hidden' : '';
        
        console.log('Состояние после:', {
            burgerMenuOpen: burgerMenu.classList.contains('open'),
            mobileMenuActive: mobileMenu.classList.contains('active'),
            overlayActive: overlay.classList.contains('active'),
            bodyOverflow: document.body.style.overflow
        });
    }
    
    function closeMenu() {
        console.log('closeMenu вызван');
        burgerMenu.classList.remove('open');
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    console.log('Меню инициализировано');
});