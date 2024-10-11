import { toggleDropdown, filterList, debounce} from './uiHelpers.js';

/**
 * This module handles form-related functionality, particularly for state and city selection.
 */

/**
 * Initializes all form handlers and event listeners.
 */
export function initializeFormHandlers() {
    const stateField = document.getElementById('state');
    const stateDropdown = document.getElementById('state-dropdown');
    const stateList = document.getElementById('state-list');

    /**
     * Fills the state field with the selected state and fetches corresponding cities.
     * @param {Event} event - The event object from the click or keypress event.
     */
    function fillState(event) {
        stateField.value = event.target.innerHTML;
        toggleDropdown(stateDropdown, false);
    }

    // Create debounced filter functions
    const filterStates = () => filterList(stateField, '.user-state');

    // Add event listeners
    stateField.addEventListener('focus', () => toggleDropdown(stateDropdown, true));
    stateField.addEventListener('blur', () => setTimeout(() => toggleDropdown(stateDropdown, false), 200));
    stateField.addEventListener('input', debounce(filterStates, 300));

    stateList.addEventListener('click', fillState);
}