let isDropdownVisible = false;

async function fetchOrganizations(query = '') {
    try {
        const url = new URL('/api/organizations', window.location.origin);
        if (query) {
            url.searchParams.append('q', query);
        }
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const organizations = await response.json();
        const orgList = document.getElementById('org-list');

        let orgCardList = document.createElement('div');
        orgCardList.classList.add('dropdown-ul');

        isDropdownVisible = organizations.results.length > 0;

        for (let org of organizations.results) {
            let orgCard = `<div class="organization-item" onclick="addOrgToForm(event)" id="${org.id}">
                                <img
                                src="${org.logo_url}"
                                alt=""
                                class="organization-logo"
                                />
                                <div class="">
                                <h4 class="bold organization-name">${org.name}</h4>
                                <div class="organization-info">
                                    <div class="organization-location">
                                    <img
                                        src="${STATIC_URLS.locationIcon}"
                                        alt="location-icon"
                                    />
                                    <p class="small-text">${org.city}, ${org.region}</p>
                                    </div>
                                    <img
                                    src="${STATIC_URLS.verticalLineIcon}"
                                    alt="vertical-line"
                                    class="d-xs-none"
                                    />
                                    <p class="small-text organization-ngo d-xs-none">EIN: ${org.ngo_id}</p>
                                </div>
                                </div>
                            </div>`;
            orgCardList.innerHTML += orgCard;
        }

        orgList.innerHTML = orgCardList.outerHTML;
        
        // Toggle dropdown visibility based on results
        toggleDropdown(orgDropdown, isDropdownVisible);

    } catch (error) {
        console.error("There was a problem fetching the organizations:", error);
        isDropdownVisible = false;
        toggleDropdown(orgDropdown, false);
        throw error;
    }
}

// Debounce function to limit API calls
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Usage example with debounce:
document.getElementById('search-org').addEventListener('input', debounce((event) => {
    const query = event.target.value;
    if (query.length >= 1) {
        fetchOrganizations(query);
    } else {
        isDropdownVisible = false;
        toggleDropdown(orgDropdown, false);
    }
}, 300)); // 300ms delay


// Close dropdown when clicking outside
// TODO: Refactor to use event delegation



document.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-parent')) {
        event.target.closest('.items-box').style.display = 'none';
        let index = event.target.closest('.items-box').dataset.id;
        if (event.target.closest('.items-box').classList.contains('causes-items')) {
            causesCheck[index].checked = false;
        }
        else if (event.target.closest('.items-box').classList.contains('skills-items')) {
            skillsCheck[index].checked = false;
        } else {
            event.target.closest('.items-box').remove();
        }
    }
});


// ADD BUSINESS TO FORM ON CLICK

addOrgToForm = (event) => {
    let orgItem = event.target.closest('.organization-item');
    let orgImg = orgItem.querySelector('.organization-logo');
    let orgName = orgItem.querySelector('.organization-name').textContent;
    orgName = (orgName.length > 20) ? orgName.slice(0, 20) + '...' : orgName;
    let orgId = orgItem.id;

    let orgBox = document.createElement('div');
    orgBox.classList.add('organization-items-box', 'items-box', 'clickable');
    // 
    orgBox.innerHTML = `
        <div class="icons-text">
            <img
                src="${orgImg.src}"
                alt=""
                class="organization-logo"
            />
            <p>${orgName}</p>
            <input type="hidden" name="plegde_organizations[]" value="${orgId}">
        </div>
        <img
            src="${STATIC_URLS.closeIcon}"
            alt="close-icon"
            class="remove-parent"
        />`;

    boxesContainer[2].style.display = 'flex';
    
    document.getElementById('org-boxes').appendChild(orgBox);
    toggleDropdown(orgDropdown, false);
}


const addManually = document.getElementById('organization-add-manually');
let userOrganization = document.getElementById('add-user-organization');
let userOrganizationForm = document.getElementById('user-organization');
let userOrganizationBtn = document.getElementById('custom-org-btn');

addManually.addEventListener('click', () => {
    userOrganization.style.display = 'block';
    addManually.style.display = 'none';
});

userOrganizationBtn.addEventListener('click', () => {
    let orgName = userOrganizationForm.value;

    if (orgName) {
        let orgBox = document.createElement('div');
        orgBox.classList.add('organization-items-box', 'items-box', 'clickable', 'add-manual-element');
        // 
        orgBox.innerHTML = `
            <div class="icons-text">
                <p>${orgName}</p>
                <input type="hidden" name="user_organizations[]" value="${orgName}">
            </div>
            <img
                src="${STATIC_URLS.closeIcon}"
                alt="close-icon"
                class="remove-parent"
            />`;

        boxesContainer[2].style.display = 'flex';
        
        document.getElementById('org-boxes').appendChild(orgBox);
        userOrganization.style.display = 'none';
        addManually.style.display = 'flex';
        userOrganizationForm.value = '';
    }
});