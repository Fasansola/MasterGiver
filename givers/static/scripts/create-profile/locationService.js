/**
 * This module handles API calls to fetch location data (states and cities).
 * It manages authentication and provides functions to fetch states and cities.
 */

let auth_token = '';
let authTokenExpiry = 0;

/**
 * Fetches and manages the authentication token for API calls.
 * @returns {Promise<string>} The authentication token.
 */
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

/**
 * Fetches the list of states from the API.
 * @returns {Promise<Array>} An array of state objects.
 */
export async function fetchStates() {
    try {
        const token = await getAuthToken();
        const statesResponse = await fetch("https://www.universal-tutorial.com/api/states/United States", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        });
        return await statesResponse.json();
    } catch (error) {
        console.error("Error fetching states:", error);
        throw error;
    }
}

/**
 * Fetches the list of cities for a given state from the API.
 * @param {string} state - The name of the state to fetch cities for.
 * @returns {Promise<Array>} An array of city objects.
 */
export async function fetchCities(state) {
    try {
        const token = await getAuthToken();
        const citiesResponse = await fetch(`https://www.universal-tutorial.com/api/cities/${state}`, {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Accept": "application/json"
            }
        });
        return await citiesResponse.json();
    } catch (error) {
        console.error("Error fetching cities:", error);
        throw error;
    }
}