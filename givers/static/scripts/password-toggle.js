document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.querySelector('#togglePassword');
    const passwords = document.querySelectorAll('.password-field');
    const eye = document.querySelector('.eye-path');

    
    togglePassword.addEventListener('click', function (e) {
        // toggle the type attribute
        passwords.forEach(password => {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            if (type === 'text')
                eye.style.fill = "#5851BF";
            else
                eye.style.fill = "#6E6D7F";
            })
        })
    });