// domElements.js

/**
 * This module exports DOM elements used across the application.
 * Centralizing these selections makes it easier to manage and update element references.
 */

export const elements = {
    causesField: document.getElementById('what-i-care-about'),
    skillsField: document.getElementById('giving-skills'),
    orgField: document.getElementById('search-org'),
    causesDropdown: document.getElementById('causes-dropdown'),
    skillsDropdown: document.getElementById('skills-dropdown'),
    orgDropdown: document.getElementById('organizations-dropdown'),
    causes: document.querySelectorAll('.causes-items'),
    causesCheck: document.querySelectorAll('.causes-check'),
    skills: document.querySelectorAll('.skills-items'),
    skillsCheck: document.querySelectorAll('.skills-check'),
    boxesContainer: document.querySelectorAll('.items-container'),
    causesBtn: document.getElementById('causes-btn'),
    skillsBtn: document.getElementById('skills-btn'),
    closeDropdown: document.getElementById('close-org-dropdown'),
};