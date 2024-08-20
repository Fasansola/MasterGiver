import re

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import User, Skill
from causes.models import Causes


# Create your views here.


def home(request):
    return render(request, 'givers/index.html')


def signup(request):
    if request.method != 'POST':
        return render(request, 'givers/register.html')

    # Collect data from the form
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    # Validate user data
    if not all([username, email, password, confirm_password]):
        return render(request, 'givers/register.html', {'error': 'All fields are required!'})

    if password != confirm_password:
        return render(request, 'givers/register.html', {'error': 'Passwords do not match!'})

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return render(request, 'givers/register.html', {'error': 'Invalid email format!'})

    # Validate username
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return render(request, 'givers/register.html', {
            'error': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores.'
        })

    # Validate password strength
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        return render(request, 'givers/register.html', {
            'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'
        })

    # Save Data to the database
    try:
        user = User.objects.create_user(username, email, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_profile')
        else:
            return render(request, 'givers/register.html', {'error': 'Failed to authenticate after registration.'})
    except IntegrityError as e:
        error_message = str(e)
        if 'username' in error_message:
            error = 'This username is already taken. Please choose a different one.'
        elif 'email' in error_message:
            error = 'This email is already registered. Please use a different email address.'
        else:
            error = 'An error occurred during registration. Please try again.'
        return render(request, 'givers/register.html', {'error': error})


@login_required
def create_profile(request):
    if request.method != 'POST':
        return render(request, 'givers/create_profile.html')

    userData = request.POST
    user = request.user

    # profile_photo = userData.get('profile_photo', '')
    profile_photo = request.FILES.get('profile_photo', '')

    if profile_photo:
        path = default_storage.save(
            'images/' + profile_photo.name, ContentFile(profile_photo.read()))
        profile_photo = path

    first_name = userData.get('first_name', '')
    last_name = userData.get('last_name', '')
    state = userData.get('state', '')
    city = userData.get('city', '')

    userInfo = User.objects.get(username=user.username)

    userInfo.profile_photo = path
    userInfo.first_name = first_name
    userInfo.last_name = last_name
    userInfo.state = state
    userInfo.city = city
    userInfo.save()
    return redirect('what_care_about')


@login_required
def what_care_about(request):
    if request.method != 'POST':
        causes = Causes.objects.all()
        skills = Skill.objects.all()
        context = {
            'causes': causes,
            'skills': skills
        }
        return render(request, 'givers/what_care_about.html', context)

    # userData = request.POST
    # user = request.user

    # skills = userData.getlist('skills', [])
    # giving_motivation = userData.get('giving_motivation', '')

    # userInfo = User.objects.get(username=user.username)

    # for skill in skills:
    #     userInfo.skills.add(skill)

    # userInfo.giving_motivation = giving_motivation
    # userInfo.save()
    # return redirect('dashboard')


def login_view(request):
    pass


def dashboard(request):
    pass


def profile(request):
    pass


def edit_profile(request):
    pass
