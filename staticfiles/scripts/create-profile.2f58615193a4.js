const stateField = document.getElementById('state');
const stateDropdown = document.getElementById('state-dropdown');
const stateList = document.getElementById('state-list');

const cityField = document.getElementById('city');
const cityDropdown = document.getElementById('city-dropdown');
const cityList = document.getElementById('city-list');

let auth_token = '';
let authTokenExpiry = 0;

function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

function toggleDropdown(dropdown, isVisible) {
    dropdown.style.visibility = isVisible ? 'visible' : 'hidden';
    dropdown.style.opacity = isVisible ? '1' : '0';
    dropdown.style.transform = isVisible ? 'translateY(0)' : 'translateY(-10px)';
}

async function getAuthToken() {
    if (Date.now() < authTokenExpiry) return auth_token;
    try {
        const tokenResponse = await fetch("https://www.universal-tutorial.com/api/getaccesstoken", {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "api-token": "KNwxBmdsxiMZ-pkO3rRkSYU6RuJNADHssVY2KwKGJxb_ZKdHYECy-iKrxib_WLlz4h8",
                "user-email": "wpxstudiox@gmail.com"
            }
        });
        const tokenData = await tokenResponse.json();
        auth_token = tokenData.auth_token;
        authTokenExpiry = Date.now() + (23 * 60 * 60 * 1000); // Set expiry to 23 hours
        return auth_token;
    } catch (error) {
        console.error("Error fetching auth token:", error);
        throw error;
    }
}

async function fetchState() {
    try {
        const token = await getAuthToken();
        const statesResponse = await fetch("https://www.universal-tutorial.com/api/states/United States", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        });
        const states = await statesResponse.json();
        stateList.innerHTML = states.map(state => 
            `<li class="user-state" tabindex="0">${state.state_name}</li>`
        ).join('');
        
        addKeyboardNavigation(stateList, '.user-state', fillState);
    } catch (error) {
        console.error("Error fetching states:", error);
    }
}

async function fetchCity(state) {
    try {
        const token = await getAuthToken();
        cityList.innerHTML = '';
        const citiesResponse = await fetch(`https://www.universal-tutorial.com/api/cities/${state}`, {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        });
        const cities = await citiesResponse.json();
        cityList.innerHTML = cities.map(city => 
            `<li class="user-city" tabindex="0">${city.city_name}</li>`
        ).join('');
        
        addKeyboardNavigation(cityList, '.user-city', fillCity);
    } catch (error) {
        console.error("Error fetching cities:", error);
    }
}

function addKeyboardNavigation(list, selector, fillFunction) {
    list.querySelectorAll(selector).forEach(item => {
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                fillFunction(e);
            }
        });
    });
}

function filterList(inputField, itemSelector) {
    const filter = inputField.value.toUpperCase();
    const items = document.querySelectorAll(itemSelector);
    items.forEach(item => {
        item.style.display = item.innerHTML.toUpperCase().includes(filter) ? '' : 'none';
    });
}

const filterStates = () => filterList(stateField, '.user-state');
const filterCities = () => filterList(cityField, '.user-city');

function fillState(event) {
    stateField.value = event.target.innerHTML;
    cityField.value = '';
    cityField.disabled = false;
    fetchCity(stateField.value);
    toggleDropdown(stateDropdown, false);
}

function fillCity(event) {
    cityField.value = event.target.innerHTML;
    toggleDropdown(cityDropdown, false);
}

// Event Listeners
stateField.addEventListener('focus', () => toggleDropdown(stateDropdown, true));
stateField.addEventListener('blur', () => setTimeout(() => toggleDropdown(stateDropdown, false), 200));
stateField.addEventListener('input', debounce(filterStates, 300));

cityField.addEventListener('focus', () => toggleDropdown(cityDropdown, true));
cityField.addEventListener('blur', () => setTimeout(() => toggleDropdown(cityDropdown, false), 200));
cityField.addEventListener('input', debounce(filterCities, 300));

stateList.addEventListener('click', fillState);
cityList.addEventListener('click', fillCity);

// Initial fetch
fetchState();
