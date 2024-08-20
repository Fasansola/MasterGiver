const url = 'https://api.pledge.to/v1/organizations'

async function fetchOrganizations() {
        const organizationsResponse = await fetch(url, {
            method: "GET", 
            headers: {
                "Authorization": "Bearer 29c10dc12b4e172f2ed14b99ae20b162", 
                "Accept": "application/json"
            }});
            const organizations = await organizationsResponse.json();
            console.log(organizations);
        };



fetchOrganizations();