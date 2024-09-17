from django.conf import settings
import re
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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
    username = request.POST.get('username').strip()
    email = request.POST.get('email').strip()
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

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

    profile_photo = request.FILES.get('profile_photo')

    if profile_photo:
        path = default_storage.save(
            'images/' + profile_photo.name, ContentFile(profile_photo.read()))
        # profile_photo = path

    first_name = userData.get('first_name')
    last_name = userData.get('last_name')
    state = userData.get('state')
    city = userData.get('city')
    about_me = userData.get('about_me')

    userInfo = User.objects.get(username=user.username)

    userInfo.profile_photo = path
    userInfo.first_name = first_name
    userInfo.last_name = last_name
    userInfo.state = state
    userInfo.city = city
    userInfo.about_me = about_me
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
    user = request.user

    why_i_give = userData.get('why_i_give')
    causes = userData.getlist('causes')
    skills = userData.getlist('skills')
    pledge_organizations = userData.getlist('pledge_organizations[]')
    user_organizations = userData.getlist('user_organizations[]')

    userInfo = User.objects.get(username=user.username)
    userInfo.giving_motivation = why_i_give
    userInfo.save()

    # For causes
    userCause, created = UserCauses.objects.get_or_create(user=userInfo)
    for cause in causes:
        cause_obj = Causes.objects.get(id=cause)
        userCause.cause.add(cause_obj)

    # For skills
    userSkill, created = UserSkills.objects.get_or_create(user=userInfo)
    for skill in skills:
        skill_obj = Skill.objects.get(id=skill)
        userSkill.skill.add(skill_obj)

    userPledgeOrg, created = UsersPledgeOrganizations.objects.get_or_create(
        user=userInfo)
    for organization in pledge_organizations:
        if PledgeOrganizations.objects.filter(id=organization).exists():
            org = PledgeOrganizations.objects.get(id=organization)
        else:
            org = PledgeOrganizations.objects.create(id=organization)
        userPledgeOrg.pledge_organization.add(org)

    for organization in user_organizations:
        UsersCharityOwnEvent.objects.create(
            user=userInfo, name=organization)

    return redirect('preview_profile')


@login_required
def preview_profile(request):
    user = request.user
    userInfo = User.objects.get(username=user.username)

    if request.method == 'POST':
        userData = request.POST
        userFile = request.FILES

        error = saveAllUserData(userInfo, userData, userFile)

        if error:
            causes = Causes.objects.all()
            user_causes = UserCauses.objects.get(user=userInfo).cause.all()
            skills = Skill.objects.all()
            user_skills = UserSkills.objects.get(user=userInfo).skill.all()
            pledge_organizations = UsersPledgeOrganizations.objects.get(
                user=userInfo).pledge_organization.all()
            user_organizations = UsersCharityOwnEvent.objects.filter(
                user=userInfo)

            user_pledge_orgs = fetch_user_organization(pledge_organizations)

            context = {
                'user': userInfo,
                'causes': causes,
                'user_causes': user_causes,
                'skills': skills,
                'user_skills': user_skills,
                'pledge_organizations': user_pledge_orgs,
                'user_organizations': user_organizations,
                'error': error
            }

            return render(request, 'givers/preview_profile.html', context)

        return redirect('confirmation')

    causes = Causes.objects.all()
    user_causes = UserCauses.objects.get(user=userInfo).cause.all()
    skills = Skill.objects.all()
    user_skills = UserSkills.objects.get(user=userInfo).skill.all()
    pledge_organizations = UsersPledgeOrganizations.objects.get(
        user=userInfo).pledge_organization.all()
    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    user_pledge_orgs = fetch_user_organization(pledge_organizations)

    context = {
        'user': userInfo,
        'causes': causes,
        'user_causes': user_causes,
        'skills': skills,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations
    }

    return render(request, 'givers/preview_profile.html', context)


@login_required
def confirmation(request):
    context = {
        'login_flow': True,
    }
    return render(request, 'givers/confirmation.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    context = {}
    if request.method != 'POST':
        return render(request, 'givers/login.html')

    userData = request.POST
    username = userData.get('username')
    password = userData.get('password')

    if not all([username, password]):
        context['error'] = 'All fields are required!'
        return render(request, 'givers/login.html', context)

    try:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            context['error'] = 'Invalid username or password!'
            return render(request, 'givers/login.html', context)
    except Exception as e:
        context['error'] = str(e)
        return render(request, 'givers/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    userInfo = request.user
    causes = Causes.objects.all()
    user_causes = UserCauses.objects.get(user=userInfo).cause.all()
    user_skills = UserSkills.objects.get(user=userInfo).skill.all()
    pledge_organizations = UsersPledgeOrganizations.objects.get(
        user=userInfo).pledge_organization.all()
    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    user_pledge_orgs = fetch_user_organization(pledge_organizations, False)

    context = {
        'causes': causes,
        'user_causes': user_causes,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations,
        'is_profile': True
    }
    return render(request, 'givers/dashboard.html', context)


def profile(request, username):
    userInfo = User.objects.get(username=username)
    causes = Causes.objects.all()
    user_causes = UserCauses.objects.get(user=userInfo).cause.all()
    user_skills = UserSkills.objects.get(user=userInfo).skill.all()
    pledge_organizations = UsersPledgeOrganizations.objects.get(
        user=userInfo).pledge_organization.all()
    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    user_pledge_orgs = fetch_user_organization(pledge_organizations, False)

    context = {
        'user': userInfo,
        'causes': causes,
        'user_causes': user_causes,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations,
        'is_profile': True
    }

    return render(request, 'givers/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    userInfo = User.objects.get(username=user.username)

    if request.method != 'POST':
        causes = Causes.objects.all()
        user_causes = UserCauses.objects.get(user=userInfo).cause.all()
        skills = Skill.objects.all()
        user_skills = UserSkills.objects.get(user=userInfo).skill.all()
        pledge_organizations = UsersPledgeOrganizations.objects.get(
            user=userInfo).pledge_organization.all()
        user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

        user_pledge_orgs = fetch_user_organization(pledge_organizations)

        context = {
            'page': 'edit_profile',
            'user': userInfo,
            'causes': causes,
            'user_causes': user_causes,
            'skills': skills,
            'user_skills': user_skills,
            'pledge_organizations': user_pledge_orgs,
            'user_organizations': user_organizations
        }
        return render(request, 'givers/edit_profile.html', context)

    userData = request.POST
    userFile = request.FILES

    error = saveAllUserData(userInfo, userData, userFile)

    if error:
        causes = Causes.objects.all()
        user_causes = UserCauses.objects.get(user=userInfo).cause.all()
        skills = Skill.objects.all()
        user_skills = UserSkills.objects.get(user=userInfo).skill.all()
        pledge_organizations = UsersPledgeOrganizations.objects.get(
            user=userInfo).pledge_organization.all()
        user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

        user_pledge_orgs = fetch_user_organization(pledge_organizations)

        context = {
            'user': userInfo,
            'causes': causes,
            'user_causes': user_causes,
            'skills': skills,
            'user_skills': user_skills,
            'pledge_organizations': user_pledge_orgs,
            'user_organizations': user_organizations,
            'error': error
        }

        return render(request, 'givers/preview_profile.html', context)

    return redirect('dashboard')

@login_required
def change_password(request):
    if request.method != 'POST':
        context = {
            'page': 'change_password'
        }
        return render(request, 'givers/change_password.html', context)

    userData = request.POST
    userInfo = request.user

    context = {
        'page': 'change_password',
        'error': updatePassword(request, userData, userInfo)
    }

    return render(request, 'givers/change_password.html', context)


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    context = {}
    if request.method != 'POST':
        return render(request, 'givers/forgot_password.html', context)

    userData = request.POST
    email = userData.get('email')

    if not email:
        context['error'] = 'Input email so we can verify your email!'
        return render(request, 'givers/forgot_password.html', context)


@login_required
@require_POST
def clear_profile_picture(request):
    user = request.user
    userInfo = User.objects.get(username=user.username)
    if  userInfo.profile_photo:
         userInfo.profile_photo.delete(save=True)
    return JsonResponse({'status': 'success'})


# FETCH ORGANIZATION

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
    query = request.GET.get('q')

    # Add the query parameter to the API request if it's not empty
    params = {'q': query} if query else {}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def fetch_user_organization(pledge_organizations, dashboard=True):
    user_pledge_orgs = []
    for org in pledge_organizations:
        api_url = f'https://api.pledge.to/v1/organizations/{org.id}'
        headers = {
            "Authorization": f"Bearer {settings.PLEDGE_API_TOKEN}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            org_data = response.json()
            org.name = org_data['name'][:20] + '...' if (len(org_data['name']) > 20 and dashboard) else org_data['name']
            org.website = org_data['website_url']
            org.logo = org_data['logo_url']
            org.save()
            user_pledge_orgs.append(org)
        except requests.RequestException as e:
            logger.error(
                f"Failed to fetch organization data for {org.id}: {e}")

    return user_pledge_orgs


# HELPER FUNCTIONS

# SAVE ALL USER DATA
def saveAllUserData(userInfo, userData, userFile):
    # Reset users custom organizations
    UsersCharityOwnEvent.objects.filter(user=userInfo).delete()

    userInfo.profile_photo = userFile.get(
        'profile_photo', userInfo.profile_photo)
    fullName = userData.get('fullname').split(' ')
    userInfo.first_name = fullName[0]
    userInfo.last_name = fullName[1]
    userInfo.state = userData.get('state')
    userInfo.city = userData.get('city')
    userInfo.about_me = userData.get('about_me')
    userInfo.giving_motivation = userData.get('why_i_give')
    userInfo.save()

    causes = userData.getlist('causes')
    skills = userData.getlist('skills')
    pledge_organizations = userData.getlist('pledge_organizations[]')

    user_organizations = userData.getlist('user_organizations[]')

    for organization in pledge_organizations:
        if not PledgeOrganizations.objects.filter(id=organization).exists():
            PledgeOrganizations.objects.create(id=organization)

    for organization in user_organizations:
        UsersCharityOwnEvent.objects.create(
            user=userInfo, name=organization)

    new_causes = Causes.objects.filter(id__in=causes)
    new_skills = Skill.objects.filter(id__in=skills)
    new_pledge_orgs = PledgeOrganizations.objects.filter(
        id__in=pledge_organizations)

    user_causes = UserCauses.objects.get(user=userInfo)
    user_skills = UserSkills.objects.get(user=userInfo)
    user_pledge_orgs = UsersPledgeOrganizations.objects.get(user=userInfo)

    user_skills.skill.set(new_skills)
    user_causes.cause.set(new_causes)
    user_pledge_orgs.pledge_organization.set(new_pledge_orgs)

    return False  # No error


# UPDATE PASSWORDS
def updatePassword(request, userData, userInfo):
    password = userData.get('password')
    new_password = userData.get('new_password')
    confirm_new_password = userData.get('confirm_new_password')

    if not userInfo.check_password(password):
        return 'Your old password was entered incorrectly. Please enter it again.'

    if new_password != confirm_new_password:
        return 'Passwords do not match!'

    # Validate password strength
    if len(new_password) < 8 or not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'\d', new_password):
        return 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'

    userInfo.set_password(new_password)

    # Update the session to prevent the user from being logged out
    update_session_auth_hash(request, userInfo)

    return False  # No error
