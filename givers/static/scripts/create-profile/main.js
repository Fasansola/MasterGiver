// main.js

import { initializeImageUpload } from './imageUpload.js';
import { fetchStates } from './locationService.js';
import { addKeyboardNavigation } from './uiHelpers.js';
import { initializeFormHandlers } from './formHandlers.js';

/**
 * This is the main entry point for the application.
 * It initializes all necessary components and sets up the initial state.
 */

/**
 * Initializes the application by setting up all necessary components.
 */
async function initialize() {
    // Initialize image upload functionality
    initializeImageUpload();

    // Initialize form handlers for state and city selection
    initializeFormHandlers();

    // Fetch and populate the list of states
    const stateList = document.getElementById('state-list');
    try {
        const states = await fetchStates();
        stateList.innerHTML = states.map(state => 
            `<li class="user-state" tabindex="0">${state.state_name}</li>`
        ).join('');

        // Add keyboard navigation to the state list
        addKeyboardNavigation(stateList, '.user-state', fillState);
    } catch (error) {
        console.error("Error initializing states:", error);
    }
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initialize);