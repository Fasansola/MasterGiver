// DOM Elements
const causesField = document.getElementById('what_i_care_about');
const skillsField = document.getElementById('giving_skills');
const orgField = document.getElementById('search-org');
const causesDropdown = document.getElementById('causes-dropdown');
const skillsDropdown = document.getElementById('skills-dropdown');
const orgDropdown = document.getElementById('organizations-dropdown');

const causes = document.querySelectorAll('.causes-items');
const causesCheck = document.querySelectorAll('.causes-check');
const skills = document.querySelectorAll('.skills-items');
const skillsCheck = document.querySelectorAll('.skills-check');
const boxesContainer = document.querySelectorAll('.items-container');

// Utility Functions

/**
 * Debounce function to limit the rate at which a function can fire.
 * @param {Function} func - The function to debounce
 * @param {number} delay - The delay in milliseconds
 * @returns {Function} - The debounced function
 */
function debounce(func, delay) {
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
function filterList(inputField, itemSelector) {
    const filter = inputField.value.toUpperCase();
    const items = document.querySelectorAll(itemSelector);
    items.forEach(item => {
        item.parentNode.style.display = item.value.toUpperCase().includes(filter) ? '' : 'none';
    });
}

/**
 * Toggles the visibility of a dropdown
 * @param {HTMLElement} dropdown - The dropdown element
 * @param {boolean} isVisible - Whether the dropdown should be visible
 */
function toggleDropdown(dropdown, isVisible) {
    dropdown.style.visibility = isVisible ? 'visible' : 'hidden';
    dropdown.style.opacity = isVisible ? '1' : '0';
    dropdown.style.transform = isVisible ? 'translateY(0)' : 'translateY(-10px)';
}

// Event Handlers

/**
 * Handles the click event for the causes button
 */
function handleCausesButtonClick() {
    causesCheck.forEach((cause, index) => {
        causes[index].style.display = cause.checked ? 'flex' : '';
        if (cause.checked) {
            causes[index].dataset.id = index;
        }
    });
    boxesContainer[0].style.display = 'flex';
    causesField.value = '';
    toggleDropdown(causesDropdown, false);
    filterList(causesField, '.causes-check');
}

/**
 * Handles the click event for the skills button
 */
function handleSkillsButtonClick() {
    skillsCheck.forEach((skill, index) => {
        skills[index].style.display = skill.checked ? 'flex' : '';
        if (skill.checked) {
            skills[index].dataset.id = index;
        }
    });
    boxesContainer[1].style.display = 'flex';
    skillsField.value = '';
    toggleDropdown(skillsDropdown, false);
    filterList(skillsField, '.skills-check');
}

/**
 * Handles clicks outside of dropdowns to close them
 * @param {Event} event - The click event
 */
function handleOutsideClick(event) {
    if (!event.target.classList.contains('skill-causes-items')) {
        if (event.target.matches(':focus') && event.target.id !== "what_i_care_about")
            toggleDropdown(causesDropdown, false);
        if (event.target.matches(':focus') && event.target.id !== "giving_skills")
            toggleDropdown(skillsDropdown, false);
        if (event.target.matches(':focus') && event.target.id !== "search-org")
            toggleDropdown(orgDropdown, false);
    }
}

// Event Listeners
document.getElementById('causes-btn').addEventListener('click', handleCausesButtonClick);
document.getElementById('skills-btn').addEventListener('click', handleSkillsButtonClick);
document.addEventListener('click', handleOutsideClick);

causesField.addEventListener('input', debounce(() => filterList(causesField, '.causes-check'), 100));
skillsField.addEventListener('input', debounce(() => filterList(skillsField, '.skills-check'), 100));

causesField.addEventListener('focus', () => toggleDropdown(causesDropdown, true));
skillsField.addEventListener('focus', () => toggleDropdown(skillsDropdown, true));