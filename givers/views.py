from django.conf import settings
import re
import requests
import json
import random

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.contenttypes.models import ContentType

from .models import User, Skill, UserSkills, UserCauses, UsersPledgeOrganizations, UsersCharityOwnEvent, GivingStyle
from causes.models import Causes
from organizations.models import PledgeOrganizations


import logging
logger = logging.getLogger(__name__)


# Create your views here.


def home(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')

    context = {
        "page_id": 'home',
        "page_type": 'static',
        "page_title": 'MasterGiver | Showcase Your Giving and Track Your Impact',
        "page_description": "Join MasterGiver, the platform that helps you showcase your giving, track your impact, and connect with meaningful causes. Build your profile today and show off your good side!",
        'index': True,
    }
    return render(request, 'givers/index.html', context)


def about(request):
    context = {
        'page_id': 'about',
        "page_type": 'static',
        "page_title": 'About Us | MasterGiver - Empowering Givers to Make an Impact',
        "page_description": "Learn about MasterGiver, the platform that empowers you to showcase your giving, track your impact, and connect with meaningful causes. Discover our mission to build a global community of givers",
        'index': True,
    }
    return render(request, 'givers/about.html', context)


def faq(request):
    context = {
        'page_id': 'faq',
        "page_type": 'static',
        "page_title": 'FAQs | MasterGiver - Your Questions Answered',
        "page_description": "Find answers to common questions about MasterGiver. Learn how to create a profile, track your giving, and connect with causes today.",
        'index': True,
    }
    return render(request, 'givers/faq.html', context)


def terms(request):
    return render(request, 'givers/terms.html', context={'page_id': 'terms', "page_type": 'static'})


def privacy(request):
    return render(request, 'givers/privacy.html', context={'page_id': 'privacy', "page_type": 'static'})


def signup(request):
    if request.method != 'POST':
        context = {
            'is_signup_flow': True
        }
        return render(request, 'givers/register.html', context)

    # Collect data from the form
    userData = json.loads(request.body)
    first_name = userData.get('first_name')
    last_name = userData.get('last_name')
    email = userData.get('email').strip()
    password = userData.get('password')
    confirm_password = userData.get('confirm_password')
    username = first_name + last_name

    if User.objects.filter(username=username):
        username = generateSpareUsername(username)

    # Validate user data
    if not all([first_name, last_name, email, password, confirm_password]):
        return JsonResponse({'error': 'All fields are required!'}, status=400)

    if password != confirm_password:
        return JsonResponse({'error': 'Passwords do not match!'}, status=400)

    # Validate email format
    try:
        validate_email(email)
    except ValidationError:
        return render(request, 'givers/register.html', {'error': 'Invalid email format!'})

    # Validate password strength
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
        return JsonResponse({'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'}, status=400)

    # Save Data to the database
    try:
        user = User.objects.create_user(username, email, password)
        user = authenticate(request, username=username,
                            email=email, password=password)
        if user is not None:
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            login(request, user)
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'error': 'An error occurred during registration. Please try again.'}, status=500)
    except IntegrityError as e:
        error_message = str(e)
        if 'username' in error_message:
            error = 'This username is already taken. Please choose a different one.'
        elif 'email' in error_message:
            error = 'This email is already registered. Please use a different email address.'
        else:
            error = 'An error occurred during registration. Please try again.'
        return JsonResponse({'error': error}, status=500)


@login_required
def create_profile(request):
    if request.method != 'POST':
        context = {
            'is_signup_flow': True
        }
        return render(request, 'givers/create_profile.html', context)

    userData = request.POST
    userInfo = request.user

    profile_photo = request.FILES.get('profile_photo', userInfo.profile_photo)

    if profile_photo:
        path = default_storage.save(
            'images/' + profile_photo.name, ContentFile(profile_photo.read()))
        profile_photo = path

    userInfo.profile_photo = profile_photo
    username = userData.get('username')
    state = userData.get('state')
    city = userData.get('city')

    userInfo.username = username
    userInfo.state = state
    userInfo.city = city
    userInfo.save()
    return redirect('what_care_about')


@login_required
def what_care_about(request):
    userInfo = request.user
    if request.method != 'POST':
        causes = Causes.objects.all()
        skills = Skill.objects.all()
        # Use filter().first() instead of get()
        user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
        user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

        # If the objects exist, get all causes/skills, otherwise use an empty queryset
        user_causes = user_causes_obj.cause.all(
        ) if user_causes_obj else Causes.objects.none()
        user_skills = user_skills_obj.skill.all(
        ) if user_skills_obj else Skill.objects.none()

        context = {
            'causes': causes,
            'skills': skills,
            'user_causes': user_causes,
            'user_skills': user_skills,
            'is_signup_flow': True
        }
        return render(request, 'givers/profile-setup.html', context)

    userData = request.POST

    why_i_give = userData.get('why_i_give')
    about_me = userData.get('about_me')
    causes = userData.getlist('causes')
    skills = userData.getlist('skills')
    pledge_organizations = userData.getlist('pledge_organizations[]')
    user_organizations = userData.getlist('user_organizations[]')

    userInfo.about_me = about_me
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
    skills = Skill.objects.all()

    # Use filter().first() instead of get()
    user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
    user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

    # If the objects exist, get all causes/skills, otherwise use an empty queryset
    user_causes = user_causes_obj.cause.all(
    ) if user_causes_obj else Causes.objects.none()
    user_skills = user_skills_obj.skill.all(
    ) if user_skills_obj else Skill.objects.none()

    # Handle potential ObjectDoesNotExist exception
    try:
        pledge_organizations = UsersPledgeOrganizations.objects.get(
            user=userInfo).pledge_organization.all()
    except ObjectDoesNotExist:
        pledge_organizations = []

    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    # Handle potential exception in fetch_user_organization function
    try:
        user_pledge_orgs = fetch_user_organization(pledge_organizations, False)
    except Exception:
        redirect('what_care_about')

    context = {
        'user': userInfo,
        'causes': causes,
        'user_causes': user_causes,
        'skills': skills,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations,
        'is_signup_flow': True
    }

    return render(request, 'givers/preview_profile.html', context)


@login_required
def confirmation(request):
    if request.method == 'POST':
        userData = request.POST
        userInfo = request.user
        giving_style = userData.get('giving_style')
        userInfo.giving_style = GivingStyle.objects.get(name=giving_style)
        userInfo.save()
        print(userInfo.giving_style)

        return redirect('dashboard')

    giving_styles = GivingStyle.objects.all()
    context = {
        'giving_styles': giving_styles,
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
    email = userData.get('email')
    password = userData.get('password')

    if not all([email, password]):
        context['error'] = 'All fields are required!'
        return render(request, 'givers/login.html', context)

    try:
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            context['error'] = 'Invalid email or password!'
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
    
    # Check if this is the first visit
    first_visit = not request.session.get('has_visited', False)
    
    # Mark as visited
    request.session['has_visited'] = True

    # Use filter().first() instead of get()
    user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
    user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

    # If the objects exist, get all causes/skills, otherwise use an empty queryset
    user_causes = user_causes_obj.cause.all(
    ) if user_causes_obj else Causes.objects.none()
    user_skills = user_skills_obj.skill.all(
    ) if user_skills_obj else Skill.objects.none()

    # Handle potential ObjectDoesNotExist exception
    try:
        pledge_organizations = UsersPledgeOrganizations.objects.get(
            user=userInfo).pledge_organization.all()
    except ObjectDoesNotExist:
        pledge_organizations = []

    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    # Handle potential exception in fetch_user_organization function
    try:
        user_pledge_orgs = fetch_user_organization(pledge_organizations, False)
    except Exception:
        user_pledge_orgs = []

    context = {
        'userInfo': userInfo,
        'causes': causes,
        'user_causes': user_causes,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations,
        'is_profile': False,
        'is_dashboard': True,
        'index': False,
        'show_welcome': first_visit,
    }
    return render(request, 'givers/dashboard.html', context)


def profile(request, username):
    userInfo = User.objects.get(username=username)
    causes = Causes.objects.all()

    # Use filter().first() instead of get()
    user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
    user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

    # If the objects exist, get all causes/skills, otherwise use an empty queryset
    user_causes = user_causes_obj.cause.all(
    ) if user_causes_obj else Causes.objects.none()
    user_skills = user_skills_obj.skill.all(
    ) if user_skills_obj else Skill.objects.none()

    pledge_organizations = UsersPledgeOrganizations.objects.get(
        user=userInfo).pledge_organization.all()
    user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

    user_pledge_orgs = fetch_user_organization(pledge_organizations, False)

    context = {
        'userInfo': userInfo,
        'causes': causes,
        'user_causes': user_causes,
        'user_skills': user_skills,
        'pledge_organizations': user_pledge_orgs,
        'user_organizations': user_organizations,
        'is_profile': True,
        'index': True,
        'page_title': f"{userInfo.first_name} {userInfo.last_name} | MasterGiver Profile | Showcase Your Impact",
        'page_description': f"Discover {userInfo.first_name} {userInfo.last_name}'s MasterGiver profile showcasing my charitable giving, volunteer work, and community impact."
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
            'user_organizations': user_organizations,
            'index': False,
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
            'index': False,
            'error': error
        }

        return render(request, 'givers/preview_profile.html', context)

    return redirect('dashboard')


@login_required
def change_password(request):
    if request.method != 'POST':
        context = {
            'page': 'change_password',
            'index': False
        }
        return render(request, 'givers/change_password.html', context)

    userData = request.POST
    userInfo = request.user

    context = {
        'page': 'change_password',
        'index': False,
        'error': updatePassword(request, userData, userInfo)
    }

    return render(request, 'givers/change_password.html', context)


@login_required
@require_POST
def clear_profile_picture(request):
    user = request.user
    userInfo = User.objects.get(username=user.username)
    if userInfo.profile_photo:
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
            org.name = org_data['name'][:20] + '...' if (
                len(org_data['name']) > 20 and dashboard) else org_data['name']
            org.website = org_data['website_url']
            org.logo = org_data['logo_url']
            org.save()
            user_pledge_orgs.append(org)
        except requests.RequestException as e:
            logger.error(
                f"Failed to fetch organization data for {org.id}: {e}")

    return user_pledge_orgs


# HELPER FUNCTIONS

def generateSpareUsername(username):
    newUsername = username + str(random.randint(0, 100))

    if User.objects.filter(username=newUsername):
        generateSpareUsername(username)
    return newUsername


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
