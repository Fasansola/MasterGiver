const mobileHamburger = document.getElementById('hamburger-menu') 
const mobileClose = document.getElementById('close-menu')
const mobileMenu = document.getElementById('mobile-menu')


mobileHamburger.addEventListener('click', closeMenu)
mobileMenu.addEventListener('click', closeMenu)


function closeMenu() {
    mobileMenu.classList.toggle('menu-not-is-visible')
    mobileMenu.classList.toggle('menu-is-visible')
}