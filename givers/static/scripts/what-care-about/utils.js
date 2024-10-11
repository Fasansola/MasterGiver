/**
 * This module contains utility functions used across the application.
 */

/**
 * Debounce function to limit the rate at which a function can fire.
 * @param {Function} func - The function to debounce
 * @param {number} delay - The delay in milliseconds
 * @returns {Function} - The debounced function
 */
export function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Filters a list based on input value
 * @param {HTMLElement} inputField - The input field element
 * @param {string} itemSelector - The selector for items to filter
 */
export function filterList(inputField, itemSelector) {
    const filter = inputField.value.toUpperCase();
    const items = document.querySelectorAll(itemSelector);
    items.forEach(item => {
        item.parentNode.style.display = item.parentNode.querySelector('.icons-text').textContent.toUpperCase().includes(filter) ? 'flex' : 'none';
    });
}

/**
 * Toggles the visibility of a dropdown
 * @param {HTMLElement} dropdown - The dropdown element
 * @param {boolean} isVisible - Whether the dropdown should be visible
 */
export function toggleDropdown(dropdown, isVisible) {
    dropdown.style.visibility = isVisible ? 'visible' : 'hidden';
    dropdown.style.opacity = isVisible ? '1' : '0';
    dropdown.style.transform = isVisible ? 'translateY(0)' : 'translateY(-10px)';
}