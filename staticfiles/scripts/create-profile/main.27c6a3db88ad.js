// main.js

import { initializeImageUpload } from './imageUpload.js';
import { addKeyboardNavigation } from './uiHelpers.js';
import { initializeFormHandlers } from './formHandlers.js';


const usStates = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
    'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
    'District of Columbia'
  ];


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
        const states = usStates;
        stateList.innerHTML = states
            .map(state => 
                `<li class="user-state" tabindex="0">${state}</li>`
            ).join('');
    
        // Add keyboard navigation to the state list
        addKeyboardNavigation(stateList, '.user-state', fillState);
    } catch (error) {
        console.error("Error initializing states:", error);
    }
}

// Initialize the application when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initialize);