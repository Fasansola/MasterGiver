form = document.getElementById('signup-form');
submitBtn = document.getElementById('submit-form');


submitBtn.addEventListener('click', async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries());
    console.log(formObject);
    const response = await fetch('/signup/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formObject),
    });
    if (response.ok) {
        window.location.href = '/create-profile';
    } else {
        const error = await response.json();
        document.getElementById('form-error').classList.toggle('d-none');
        document.getElementById('form-error').classList.toggle('d-flex');
        document.getElementById('error-text').innerText = error.error;
    }
});