// eventHandlers.js

import { elements } from './domElements.js';
import { filterList, toggleDropdown } from './utils.js';

/**
 * This module contains event handler functions for various user interactions.
 */

/**
 * Handles the click event for the causes button
 */
export function handleCausesButtonClick() {
    elements.causesCheck.forEach((cause, index) => {
        elements.causes[index].style.display = cause.checked ? 'flex' : 'none';
        if (cause.checked) {
            elements.causes[index].dataset.id = index;
        }
    });
    elements.boxesContainer[0].style.display = 'flex';
    elements.causesField.value = '';
    toggleDropdown(elements.causesDropdown, false);
    filterList(elements.causesField, '.causes-check');
}

/**
 * Handles the click event for the skills button
 */
export function handleSkillsButtonClick() {
    elements.skillsCheck.forEach((skill, index) => {
        elements.skills[index].style.display = skill.checked ? 'flex' : 'none';
        if (skill.checked) {
            elements.skills[index].dataset.id = index;
        }
    });
    elements.boxesContainer[1].style.display = 'flex';
    elements.skillsField.value = '';
    toggleDropdown(elements.skillsDropdown, false);
    filterList(elements.skillsField, '.skills-check');
}

/**
 * Handles clicks outside of dropdowns to close them
 * @param {Event} event - The click event
 */
export function handleOutsideClick(event) {
    if (!event.target.classList.contains('skill-causes-items')) {
        if (event.target.matches(':focus') && event.target.id !== "what-i-care-about")
            toggleDropdown(elements.causesDropdown, false);
        if (event.target.matches(':focus') && event.target.id !== "giving-skills")
            toggleDropdown(elements.skillsDropdown, false);
        if (event.target.matches(':focus') && event.target.id !== "search-org")
            toggleDropdown(elements.orgDropdown, false);
    }
}