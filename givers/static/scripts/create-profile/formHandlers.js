import { toggleDropdown, filterList, addKeyboardNavigation, debounce} from './uiHelpers.js';
import { fetchCities } from './locationService.js';

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

    const cityField = document.getElementById('city');
    const cityDropdown = document.getElementById('city-dropdown');
    const cityList = document.getElementById('city-list');

    /**
     * Fills the state field with the selected state and fetches corresponding cities.
     * @param {Event} event - The event object from the click or keypress event.
     */
    function fillState(event) {
        stateField.value = event.target.innerHTML;
        cityField.value = '';
        cityField.disabled = false;
        fetchCity(stateField.value);
        toggleDropdown(stateDropdown, false);
    }

    /**
     * Fills the city field with the selected city.
     * @param {Event} event - The event object from the click or keypress event.
     */
    function fillCity(event) {
        cityField.value = event.target.innerHTML;
        toggleDropdown(cityDropdown, false);
    }

    /**
     * Fetches cities for a given state and populates the city dropdown.
     * @param {string} state - The name of the state to fetch cities for.
     */
    async function fetchCity(state) {
        try {
            const cities = await fetchCities(state);
            cityList.innerHTML = cities.map(city => 
                `<li class="user-city" tabindex="0">${city.city_name}</li>`
            ).join('');

            addKeyboardNavigation(cityList, '.user-city', fillCity);
        } catch (error) {
            console.error("Error fetching cities:", error);
        }
    }

    // Create debounced filter functions
    const filterStates = () => filterList(stateField, '.user-state');
    const filterCities = () => filterList(cityField, '.user-city');

    // Add event listeners
    stateField.addEventListener('focus', () => toggleDropdown(stateDropdown, true));
    stateField.addEventListener('blur', () => setTimeout(() => toggleDropdown(stateDropdown, false), 200));
    stateField.addEventListener('input', debounce(filterStates, 300));

    cityField.addEventListener('focus', () => toggleDropdown(cityDropdown, true));
    cityField.addEventListener('blur', () => setTimeout(() => toggleDropdown(cityDropdown, false), 200));
    cityField.addEventListener('input', debounce(filterCities, 300));

    stateList.addEventListener('click', fillState);
    cityList.addEventListener('click', fillCity);
}