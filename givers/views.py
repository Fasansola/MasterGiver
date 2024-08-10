import re

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import User


# Create your views here.


def home(request):
    return render(request, 'givers/index.html')


def signup(request):
    if request.method == 'POST':

        # Collect data from the form
        userData = request.POST
        username = userData.get('username', '').strip()
        email = userData.get('email', '').strip()
        password = userData.get('password', '')
        confirm_password = userData.get('confirm_password', '')

        # Validate user data
        if not all([username, email, password, confirm_password]):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match!'}, status=400)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format!'}, status=400)

        # Validate username (example: only alphanumeric characters and underscores, 3-20 characters long)
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return JsonResponse({'error': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores.'}, status=400)

        # Validate password strength (example: at least 8 characters, including uppercase, lowercase, and numbers)
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return JsonResponse({'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'}, status=400)

        # Save Data to the database
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            error_message = str(e)
            if 'username' in error_message:
                return JsonResponse({'error': 'This username is already taken. Please choose a different one.'}, status=409)
            elif 'email' in error_message:
                return JsonResponse({'error': 'This email is already registered. Please use a different email address.'}, status=409)
            else:
                return JsonResponse({'error': 'An error occurred during registration. Please try again.'}, status=500)

        return JsonResponse({'success': 'Thanks for signing up!'}, status=201)

    return render(request, 'givers/register.html')


def login(request):
    pass


def dashboard(request):
    pass


def profile(request):
    pass


def edit_profile(request):
    pass
