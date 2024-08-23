from django.conf import settings
import re
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.contenttypes.models import ContentType

from .models import User, Skill, UserSkills, UserCauses, UsersPledgeOrganizations, UsersCharityOwnEvent
from causes.models import Causes
from organizations.models import PledgeOrganizations


import logging
logger = logging.getLogger(__name__)


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

    userData = request.POST
    print(userData)
    user = request.user

    why_i_give = userData.get('why_i_give', '')
    causes = userData.getlist('causes', [])
    skills = userData.getlist('skills', [])
    plegde_organizations = userData.getlist('plegde_organizations[]', [])
    user_organizations = userData.getlist('user_organizations[]', [])

    userInfo = User.objects.get(username=user.username)
    userInfo.giving_motivation = why_i_give
    userInfo.save()

    userCause = UserCauses.objects.create(user=userInfo)
    for cause in causes:
        cause = Causes.objects.get(id=cause)
        userCause.cause.add(cause)

    userSkill = UserSkills.objects.create(user=userInfo)
    for skill in skills:
        skill = Skill.objects.get(id=skill)
        userSkill.skill.add(skill)

    userPledgeOrg = UsersPledgeOrganizations.objects.create(user=userInfo)
    for organization in plegde_organizations:
        if PledgeOrganizations.objects.filter(id=organization).exists():
            org = PledgeOrganizations.objects.get(id=organization)
        else:
            org = PledgeOrganizations.objects.create(id=organization)
        userPledgeOrg.pledge_organization.add(org)

    for organization in user_organizations:
        UsersCharityOwnEvent.objects.create(
            user=userInfo, name=organization)

    return HttpResponse('Data received')
    # return redirect('dashboard')


@login_required
def preview_profile(request):
    user = request.user
    userInfo = User.objects.get(username=user.username)
    causes = UserCauses.objects.get(user=userInfo).cause.all()
    skills = UserSkills.objects.get(user=userInfo).skill.all()
    pledge_organizations = UsersPledgeOrganizations.objects.get(
        user=userInfo).pledge_organization.all()
    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    context = {
        'user': userInfo,
        'causes': causes,
        'skills': skills,
        'pledge_organizations': pledge_organizations,
        'user_organizations': user_organizations
    }

    return render(request, 'givers/preview_profile.html', context)


def fetch_organizations(request):
    if not settings.PLEDGE_API_TOKEN:
        logger.error("PLEDGE_API_TOKEN is not set")
        return JsonResponse({"error": "API token is not configured"}, status=500)

    api_url = 'https://api.pledge.to/v1/organizations'
    headers = {
        "Authorization": f"Bearer {settings.PLEDGE_API_TOKEN}",
        "Accept": "application/json"
    }

    # Get the query parameter from the request
    query = request.GET.get('q', '')

    # Add the query parameter to the API request if it's not empty
    params = {'q': query} if query else {}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def login_view(request):
    pass


def dashboard(request):
    pass


def profile(request):
    pass


def edit_profile(request):
    pass
