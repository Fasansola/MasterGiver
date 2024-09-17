// organizationSearch.js

import { elements } from './domElements.js';
import { debounce, toggleDropdown } from './utils.js';

// Flag to track if the dropdown should be visible
let isDropdownVisible = false;

/**
 * Fetches organizations from the API based on the search query
 * @param {string} query - The search query string
 */
async function fetchOrganizations(query = '') {
    try {
        // Construct the API URL
        const url = new URL('/api/organizations', window.location.origin);
        if (query) {
            url.searchParams.append('q', query);
        }

        // Fetch data from the API
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const organizations = await response.json();
        const orgList = document.getElementById('org-list');

        // Create a container for organization cards
        let orgCardList = document.createElement('div');
        orgCardList.classList.add('dropdown-ul');

        // Set dropdown visibility based on results
        isDropdownVisible = organizations.results.length > 0;

        // Generate HTML for each organization
        for (let org of organizations.results) {
            let orgCard = `
                <div class="organization-item" data-id="${org.id}">
                    <img src="${org.logo_url}" alt="" class="organization-logo" />
                    <div class="">
                        <h4 class="bold organization-name">${org.name}</h4>
                        <div class="organization-info">
                            <div class="organization-location">
                                <img src="${STATIC_URLS.locationIcon}" alt="location-icon" />
                                <p class="small-text">${org.city}, ${org.region}</p>
                            </div>
                            <img src="${STATIC_URLS.verticalLineIcon}" alt="vertical-line" class="d-xs-none" />
                            <p class="small-text organization-ngo d-xs-none">EIN: ${org.ngo_id}</p>
                        </div>
                    </div>
                </div>`;
            orgCardList.innerHTML += orgCard;
        }

        // Update the DOM with the new organization list
        orgList.innerHTML = orgCardList.outerHTML;

        // Toggle dropdown visibility based on results
        toggleDropdown(elements.orgDropdown, isDropdownVisible);

    } catch (error) {
        console.error("There was a problem fetching the organizations:", error);
        isDropdownVisible = false;
        toggleDropdown(elements.orgDropdown, false);
        throw error;
    }
}

/**
 * Adds the selected organization to the form
 * @param {Event} event - The click event on the organization item
 */
function addOrgToForm(event) {
    let orgItem = event.target.closest('.organization-item');
    let orgImg = orgItem.querySelector('.organization-logo');
    let orgName = orgItem.querySelector('.organization-name').textContent;
    // Truncate organization name if it's too long
    orgName = (orgName.length > 20) ? orgName.slice(0, 20) + '...' : orgName;
    let orgId = orgItem.dataset.id;

    // Create a new organization box element
    let orgBox = document.createElement('div');
    orgBox.classList.add('organization-items-box', 'items-box', 'clickable');
    orgBox.innerHTML = `
        <div class="icons-text">
            <img src="${orgImg.src}" alt="" class="organization-logo" />
            <p>${orgName}</p>
            <input type="hidden" name="pledge_organizations[]" value="${orgId}">
        </div>
        <img src="${STATIC_URLS.closeIcon}" alt="close-icon" class="remove-parent" />`;

    // Display the container and add the new organization box
    elements.boxesContainer[2].style.display = 'flex';
    document.getElementById('org-boxes').appendChild(orgBox);
    
    // Hide the dropdown after selection
    toggleDropdown(elements.orgDropdown, false);
}

/**
 * Handles the manual addition of organizations
 */
function handleManualOrgAdd() {
    const addManually = document.getElementById('organization-add-manually');
    const userOrganization = document.getElementById('add-user-organization');
    const userOrganizationForm = document.getElementById('user-organization');
    const userOrganizationBtn = document.getElementById('custom-org-btn');

    // Show manual add form when "Add Manually" is clicked
    addManually.addEventListener('click', () => {
        userOrganization.style.display = 'block';
        addManually.style.display = 'none';
    });

    // Handle manual organization addition
    userOrganizationBtn.addEventListener('click', () => {
        let orgName = userOrganizationForm.value;

        if (orgName) {
            // Create a new organization box for manually added org
            let orgBox = document.createElement('div');
            orgBox.classList.add('organization-items-box', 'items-box', 'clickable', 'add-manual-element');
            orgBox.innerHTML = `
                <div class="icons-text">
                    <p>${orgName}</p>
                    <input type="hidden" name="user_organizations[]" value="${orgName}">
                </div>
                <img src="${STATIC_URLS.closeIcon}" alt="close-icon" class="remove-parent" />`;

            // Display the container and add the new organization box
            elements.boxesContainer[2].style.display = 'flex';
            document.getElementById('org-boxes').appendChild(orgBox);

            // Reset the form
            userOrganization.style.display = 'none';
            addManually.style.display = 'flex';
            userOrganizationForm.value = '';
        }
    });
}

/**
 * Initializes the organization search functionality
 * This function should be called when the DOM is ready
 */
export function initializeOrganizationSearch() {
    // Set up the search input event listener with debounce
    elements.orgField.addEventListener('input', debounce((event) => {
        const query = event.target.value;
        if (query.length >= 1) {
            fetchOrganizations(query);
        } else {
            isDropdownVisible = false;
            toggleDropdown(elements.orgDropdown, false);
        }
    }, 300)); // 300ms debounce delay

    // Set up click event listener for organization selection
    document.getElementById('org-list').addEventListener('click', (event) => {
        if (event.target.closest('.organization-item')) {
            addOrgToForm(event);
        }
    });

    // Initialize manual organization addition functionality
    handleManualOrgAdd();
}