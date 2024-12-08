// main.js

import { elements } from './domElements.js';
import { debounce, filterList, toggleDropdown } from './utils.js';
import { handleCausesButtonClick, handleSkillsButtonClick, handleOutsideClick } from './eventHandlers.js';
import { initializeOrganizationSearch } from './organizationSearch.js';

/**
 * This is the main entry point for the application.
 * It sets up event listeners and initializes the application.
 */

function initializeApp() {
    // Set up event listeners for buttons
    elements.causesBtn.addEventListener('click', handleCausesButtonClick);
    elements.skillsBtn.addEventListener('click', handleSkillsButtonClick);


    // Set up event listeners for closing organization dropdowns
    elements.closeDropdown.addEventListener('click', () => toggleDropdown(elements.orgDropdown, false));
    
    // Set up event listener for outside clicks
    document.addEventListener('click', handleOutsideClick);

    // Set up event listeners for input fields
    elements.causesField.addEventListener('input', debounce(() => filterList(elements.causesField, '.causes-check'), 100));
    elements.skillsField.addEventListener('input', debounce(() => filterList(elements.skillsField, '.skills-check'), 100));

    // Set up event listeners for focus events
    elements.causesField.addEventListener('focus', () => toggleDropdown(elements.causesDropdown, true));
    elements.skillsField.addEventListener('focus', () => toggleDropdown(elements.skillsDropdown, true));

    // Initialize organization search functionality
    initializeOrganizationSearch();

    // Set up event listener for removing items
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-parent')) {
            const itemBox = event.target.closest('.items-box');
            itemBox.style.display = 'none';
            const index = itemBox.dataset.id;
            if (itemBox.classList.contains('causes-items')) {
                elements.causesCheck[index].checked = false;
            }
            else if (itemBox.classList.contains('skills-items')) {
                elements.skillsCheck[index].checked = false;
            } else {
                itemBox.remove();
            }
        }
    });
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeApp);