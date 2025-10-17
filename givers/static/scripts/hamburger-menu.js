const mobileHamburger = document.getElementById('hamburger-menu');
const mobileClose = document.getElementById('close-menu');
const mobileMenu = document.getElementById('mobile-menu');

// Only add event listeners if elements exist
if (mobileHamburger && mobileMenu) {
    mobileHamburger.addEventListener('click', toggleMenu);
    mobileMenu.addEventListener('click', toggleMenu);
}

// If close button exists, add its event listener
if (mobileClose) {
    mobileClose.addEventListener('click', toggleMenu);
}

function toggleMenu() {
    if (mobileMenu) {
        mobileMenu.classList.toggle('menu-not-is-visible');
        mobileMenu.classList.toggle('menu-is-visible');
    }
}