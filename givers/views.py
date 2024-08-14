import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import User


# Create your views here.


def home(request):
    return render(request, 'givers/index.html')


def signup(request):
    context = {}

    if request.method != 'POST':
        return render(request, 'givers/register.html')

    # Collect data from the form
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    # Validate user data
    if not all([username, email, password, confirm_password]):
        context = {'error': 'All fields are required!'}
        return render(request, 'givers/register.html', context)

    if password != confirm_password:
        context = {'error': 'Passwords do not match!'}
        return render(request, 'givers/register.html', context)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        context = {'error': 'Invalid email format!'}
        return render(request, 'givers/register.html', context)

    # Validate username
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        context = {
            'error': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores.'}
        return render(request, 'givers/register.html', context)

    # Validate password strength
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        context = {
            'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'}
        return render(request, 'givers/register.html', context)

    # Save Data to the database
    try:
        user = User.objects.create_user(username, email, password)
        login(user)
        # JsonResponse({'success': 'Thanks for signing up!'}, status=201)
        return redirect('create_profile')
    except IntegrityError as e:
        error_message = str(e)
        if 'username' in error_message:
            context = {
                'error': 'This username is already taken. Please choose a different one.'}
            return render(request, 'givers/register.html', context)
        elif 'email' in error_message:
            context = {
                'error': 'This email is already registered. Please use a different email address.'}
            return render(request, 'givers/register.html', context)
        else:
            context = {
                'error': 'An error occurred during registration. Please try again.'}
            return render(request, 'givers/register.html', context)


@login_required
def create_profile(request):
    if request.method != 'POST':
        return render(request, 'givers/create_profile.html')


def login(request):
    pass


def dashboard(request):
    pass


def profile(request):
    pass


def edit_profile(request):
    pass
