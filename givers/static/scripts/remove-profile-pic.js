document.getElementById('clear-profile-picture').addEventListener('click', function() {
    if (confirm('Are you sure you want to clear your profile picture?')) {
        fetch(STATIC_URLS.page_url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': STATIC_URLS.csrf_token,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
});