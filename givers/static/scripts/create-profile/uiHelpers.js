/**
 * This module provides utility functions for UI interactions and enhancements.
 */

/**
 * Creates a debounced function that delays invoking `func` until after `delay` milliseconds
 * have elapsed since the last time the debounced function was invoked.
 * @param {Function} func - The function to debounce.
 * @param {number} delay - The number of milliseconds to delay.
 * @returns {Function} The debounced function.
 */
export function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Toggles the visibility of a dropdown element.
 * @param {HTMLElement} dropdown - The dropdown element to toggle.
 * @param {boolean} isVisible - Whether the dropdown should be visible.
 */
export function toggleDropdown(dropdown, isVisible) {
    dropdown.style.visibility = isVisible ? 'visible' : 'hidden';
    dropdown.style.opacity = isVisible ? '1' : '0';
    dropdown.style.transform = isVisible ? 'translateY(0)' : 'translateY(-10px)';
}

/**
 * Adds keyboard navigation to a list of items.
 * @param {HTMLElement} list - The container element for the list items.
 * @param {string} selector - The CSS selector for the list items.
 * @param {Function} fillFunction - The function to call when an item is selected.
 */
export function addKeyboardNavigation(list, selector, fillFunction) {
    list.querySelectorAll(selector).forEach(item => {
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                fillFunction(e);
            }
        });
    });
}

/**
 * Filters a list of items based on input value.
 * @param {HTMLInputElement} inputField - The input field to get the filter value from.
 * @param {string} itemSelector - The CSS selector for the list items.
 */
export function filterList(inputField, itemSelector) {
    const filter = inputField.value.toUpperCase();
    const items = document.querySelectorAll(itemSelector);
    items.forEach(item => {
        item.style.display = item.innerHTML.toUpperCase().includes(filter) ? '' : 'none';
    });
}