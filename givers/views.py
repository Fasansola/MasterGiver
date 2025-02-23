from django.conf import settings
import re
import requests
import json
import random
import logging
from typing import Optional

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

logger = logging.getLogger(__name__)


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


def generateSpareUsername(username: str) -> str:
    """Generate a unique username with error handling."""
    try:
        newUsername = username + str(random.randint(0, 100))
        if User.objects.filter(username=newUsername).exists():
            return generateSpareUsername(username)
        return newUsername
    except Exception as e:
        logger.error(f"Username generation error: {str(e)}")
        # Fallback to timestamp if needed
        return f"{username}{int(time.time())}"


def signup(request):
    if request.method != 'POST':
        context = {
            'is_signup_flow': True,
            'index': True,
        }
        return render(request, 'givers/register.html', context)

    try:
        # Collect data from the form
        userData = json.loads(request.body)
        first_name = userData.get('first_name', '').strip()
        last_name = userData.get('last_name', '').strip()
        email = userData.get('email', '').strip()
        password = userData.get('password', '')
        confirm_password = userData.get('confirm_password', '')
        username = first_name + last_name

        # Basic validation
        if not all([first_name, last_name, email, password, confirm_password]):
            return JsonResponse({'error': 'All fields are required!'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match!'}, status=400)

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Invalid email format!'}, status=400)

        # Password strength validation
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return JsonResponse({'error': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'}, status=400)

        # Generate unique username if needed
        if User.objects.filter(username=username).exists():
            username = generateSpareUsername(username)

        # Create and save user
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
            return JsonResponse({'error': 'An error occurred during registration.'}, status=500)

    except IntegrityError as e:
        error_message = str(e)
        if 'username' in error_message:
            error = 'This username is already taken. Please choose a different one.'
        elif 'email' in error_message:
            error = 'This email is already registered. Please use a different email address.'
        else:
            error = 'An error occurred during registration. Please try again.'
        return JsonResponse({'error': error}, status=400)
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred during registration.'}, status=500)


@login_required
def create_profile(request):
    if request.method != 'POST':
        context = {
            'is_signup_flow': True
        }
        return render(request, 'givers/create_profile.html', context)

    try:
        userInfo = request.user
        profile_photo = request.FILES.get('profile_photo')

        if profile_photo:
            try:
                path = default_storage.save(
                    'images/' + profile_photo.name,
                    ContentFile(profile_photo.read())
                )
                userInfo.profile_photo = path
            except Exception as e:
                logger.error(f"Profile photo save error: {str(e)}")

        username = request.POST.get('username', '').strip()
        state = request.POST.get('state', '').strip()
        city = request.POST.get('city', '').strip()

        if username:
            userInfo.username = username
        if state:
            userInfo.state = state
        if city:
            userInfo.city = city

        userInfo.save()
        return redirect('what_care_about')

    except Exception as e:
        logger.error(f"Create profile error: {str(e)}")
        context = {
            'is_signup_flow': True,
            'error': 'An error occurred while creating your profile'
        }
        return render(request, 'givers/create_profile.html', context)


@login_required
def what_care_about(request):
    userInfo = request.user
    if request.method != 'POST':
        causes = Causes.objects.all()
        skills = Skill.objects.all()

        try:
            user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
            user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

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
        except Exception as e:
            logger.error(f"Error loading what_care_about page: {str(e)}")
            return render(request, 'givers/profile-setup.html', {
                'is_signup_flow': True,
                'error': 'Error loading page'
            })

    try:
        userData = request.POST

        # Get and clean form data
        why_i_give = userData.get('why_i_give', '').strip()
        about_me = userData.get('about_me', '').strip()
        causes = userData.getlist('causes', [])
        skills = userData.getlist('skills', [])
        pledge_organizations = userData.getlist('pledge_organizations[]', [])
        user_organizations = userData.getlist('user_organizations[]', [])

        # Save user info
        userInfo.about_me = about_me
        userInfo.giving_motivation = why_i_give
        userInfo.save()

        # Handle causes
        userCause, _ = UserCauses.objects.get_or_create(user=userInfo)
        userCause.cause.clear()  # Clear existing causes
        for cause in causes:
            try:
                cause_obj = Causes.objects.get(id=cause)
                userCause.cause.add(cause_obj)
            except Causes.DoesNotExist:
                logger.warning(f"Cause with id {cause} does not exist")

        # Handle skills
        userSkill, _ = UserSkills.objects.get_or_create(user=userInfo)
        userSkill.skill.clear()  # Clear existing skills
        for skill in skills:
            try:
                skill_obj = Skill.objects.get(id=skill)
                userSkill.skill.add(skill_obj)
            except Skill.DoesNotExist:
                logger.warning(f"Skill with id {skill} does not exist")

        # Handle pledge organizations
        userPledgeOrg, _ = UsersPledgeOrganizations.objects.get_or_create(
            user=userInfo)
        userPledgeOrg.pledge_organization.clear()  # Clear existing organizations
        for organization in pledge_organizations:
            org, created = PledgeOrganizations.objects.get_or_create(
                id=organization)
            userPledgeOrg.pledge_organization.add(org)

        # Handle user organizations
        UsersCharityOwnEvent.objects.filter(
            user=userInfo).delete()  # Clear existing
        for organization in user_organizations:
            if organization.strip():  # Only create if name isn't empty
                UsersCharityOwnEvent.objects.create(
                    user=userInfo,
                    name=organization.strip()
                )

        return redirect('preview_profile')

    except Exception as e:
        logger.error(f"Error saving what_care_about data: {str(e)}")
        return render(request, 'givers/profile-setup.html', {
            'error': 'Error saving your preferences',
            'is_signup_flow': True
        })


@login_required
def preview_profile(request):
    try:
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
                    user=userInfo
                ).pledge_organization.all()
                user_organizations = UsersCharityOwnEvent.objects.filter(
                    user=userInfo)

                user_pledge_orgs = fetch_user_organization(
                    pledge_organizations)

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

        # Get user data for display
        causes = Causes.objects.all()
        skills = Skill.objects.all()

        user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
        user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

        user_causes = user_causes_obj.cause.all(
        ) if user_causes_obj else Causes.objects.none()
        user_skills = user_skills_obj.skill.all(
        ) if user_skills_obj else Skill.objects.none()

        try:
            pledge_organizations = UsersPledgeOrganizations.objects.get(
                user=userInfo
            ).pledge_organization.all()
        except ObjectDoesNotExist:
            pledge_organizations = []

        user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

        try:
            user_pledge_orgs = fetch_user_organization(
                pledge_organizations, False)
        except Exception as e:
            logger.error(f"Error fetching organizations: {str(e)}")
            return redirect('what_care_about')

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

    except Exception as e:
        logger.error(f"Error in preview_profile: {str(e)}")
        return render(request, 'givers/preview_profile.html', {
            'error': 'Error loading profile preview',
            'is_signup_flow': True
        })


@login_required
def confirmation(request):
    if request.method == 'POST':
        try:
            userData = request.POST
            userInfo = request.user
            giving_style = userData.get('giving_style')
            if giving_style:
                style_obj = GivingStyle.objects.get(name=giving_style)
                userInfo.giving_style = style_obj
                userInfo.save()
            return redirect('dashboard')
        except Exception as e:
            logger.error(f"Error saving giving style: {str(e)}")
            giving_styles = GivingStyle.objects.all()
            return render(request, 'givers/confirmation.html', {
                'giving_styles': giving_styles,
                'login_flow': True,
                'error': 'Error saving your giving style'
            })

    giving_styles = GivingStyle.objects.all()
    context = {
        'giving_styles': giving_styles,
        'login_flow': True,
    }
    return render(request, 'givers/confirmation.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method != 'POST':
        return render(request, 'givers/login.html')

    try:
        userData = request.POST
        email = userData.get('email', '').strip()
        password = userData.get('password', '')

        if not all([email, password]):
            return render(request, 'givers/login.html', {
                'error': 'All fields are required!'
            })

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'givers/login.html', {
                'error': 'Invalid email or password!'
            })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return render(request, 'givers/login.html', {
            'error': 'An error occurred during login'
        })


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    try:
        userInfo = request.user
        causes = Causes.objects.all()

        # Check if this is the first visit
        first_visit = not request.session.get('has_visited', False)
        request.session['has_visited'] = True

        # Get user causes
        user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
        user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

        # Get associated data or empty querysets
        user_causes = user_causes_obj.cause.all(
        ) if user_causes_obj else Causes.objects.none()
        user_skills = user_skills_obj.skill.all(
        ) if user_skills_obj else Skill.objects.none()

        # Get pledge organizations
        try:
            pledge_organizations = UsersPledgeOrganizations.objects.get(
                user=userInfo
            ).pledge_organization.all()
        except ObjectDoesNotExist:
            pledge_organizations = []

        user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

        try:
            user_pledge_orgs = fetch_user_organization(
                pledge_organizations, False)
        except Exception as e:
            logger.error(
                f"Error fetching organizations in dashboard: {str(e)}")
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

    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        return render(request, 'givers/dashboard.html', {
            'error': 'Error loading dashboard',
            'is_dashboard': True,
            'index': False
        })


def profile(request, username):
    try:
        userInfo = User.objects.get(username=username)
        causes = Causes.objects.all()

        # Get user causes and skills
        user_causes_obj = UserCauses.objects.filter(user=userInfo).first()
        user_skills_obj = UserSkills.objects.filter(user=userInfo).first()

        user_causes = user_causes_obj.cause.all(
        ) if user_causes_obj else Causes.objects.none()
        user_skills = user_skills_obj.skill.all(
        ) if user_skills_obj else Skill.objects.none()

        # Get organizations
        try:
            pledge_organizations = UsersPledgeOrganizations.objects.get(
                user=userInfo
            ).pledge_organization.all()
        except ObjectDoesNotExist:
            pledge_organizations = []

        user_organizations = UsersCharityOwnEvent.objects.filter(user=userInfo)

        try:
            user_pledge_orgs = fetch_user_organization(
                pledge_organizations, False)
        except Exception as e:
            logger.error(f"Error fetching organizations in profile: {str(e)}")
            user_pledge_orgs = []

        context = {
            'userInfo': userInfo,
            'causes': causes,
            'user_causes': user_causes,
            'user_skills': user_skills,
            'pledge_organizations': user_pledge_orgs,
            'user_organizations': user_organizations,
            'is_profile': True,
            'index': True,
            'page_title': f"{userInfo.first_name} {userInfo.last_name} | MasterGiver",
            'page_description': f"Discover {userInfo.first_name} {userInfo.last_name}'s MasterGiver profile showcasing my charitable giving, volunteer work, and community impact."
        }
        return render(request, 'givers/profile.html', context)

    except User.DoesNotExist:
        return render(request, 'givers/404.html', status=404)
    except Exception as e:
        logger.error(f"Profile error: {str(e)}")
        return render(request, 'givers/500.html', status=500)


@login_required
def edit_profile(request):
    try:
        user = request.user
        userInfo = User.objects.get(username=user.username)

        if request.method != 'POST':
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
                'page': 'edit_profile',  # Keeping your original context structure
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
            user_organizations = UsersCharityOwnEvent.objects.filter(
                user=userInfo)

            user_pledge_orgs = fetch_user_organization(pledge_organizations)

            context = {
                'page': 'edit_profile',  # Added back here too
                'user': userInfo,
                'causes': causes,
                'user_causes': user_causes,
                'skills': skills,
                'user_skills': user_skills,
                'pledge_organizations': user_pledge_orgs,
                'user_organizations': user_organizations,
                'error': error,
                'index': False,
            }

            return render(request, 'givers/edit_profile.html', context)

        return redirect('dashboard')

    except Exception as e:
        logger.error(f"Edit profile error: {str(e)}")
        return render(request, 'givers/edit_profile.html', {
            'error': 'Error loading or saving profile',
            'index': False,
            'page': 'edit_profile'  # Added here as well
        })


@login_required
def change_password(request):
    if request.method != 'POST':
        context = {
            'page': 'change_password',
            'index': False
        }
        return render(request, 'givers/change_password.html', context)

    try:
        userData = request.POST
        userInfo = request.user
        error = updatePassword(request, userData, userInfo)

        if error:
            context = {
                'page': 'change_password',
                'index': False,
                'error': error
            }
            return render(request, 'givers/change_password.html', context)

        return redirect('dashboard')

    except Exception as e:
        logger.error(f"Change password error: {str(e)}")
        context = {
            'page': 'change_password',
            'index': False,
            'error': 'An error occurred while changing your password'
        }
        return render(request, 'givers/change_password.html', context)


@login_required
@require_POST
def clear_profile_picture(request):
    try:
        user = request.user
        userInfo = User.objects.get(username=user.username)
        if userInfo.profile_photo:
            userInfo.profile_photo.delete(save=True)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Clear profile picture error: {str(e)}")
        return JsonResponse({'error': 'Failed to clear profile picture'}, status=500)


def fetch_organizations(request):
    if not settings.PLEDGE_API_TOKEN:
        logger.error("PLEDGE_API_TOKEN is not set")
        return JsonResponse({"error": "API token is not configured"}, status=500)

    api_url = 'https://api.pledge.to/v1/organizations'
    headers = {
        "Authorization": f"Bearer {settings.PLEDGE_API_TOKEN}",
        "Accept": "application/json"
    }

    query = request.GET.get('q', '').strip()
    params = {'q': query} if query else {}

    try:
        response = requests.get(api_url, headers=headers,
                                params=params, timeout=10)
        response.raise_for_status()
        return JsonResponse(response.json(), safe=False)
    except requests.RequestException as e:
        logger.error(f"Pledge API error: {str(e)}")
        return JsonResponse({"error": "Failed to fetch organizations"}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error in fetch_organizations: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


def fetch_user_organization(pledge_organizations, dashboard=True):
    user_pledge_orgs = []

    if not settings.PLEDGE_API_TOKEN:
        logger.error("PLEDGE_API_TOKEN is not set")
        return user_pledge_orgs

    for org in pledge_organizations:
        try:
            api_url = f'https://api.pledge.to/v1/organizations/{org.id}'
            headers = {
                "Authorization": f"Bearer {settings.PLEDGE_API_TOKEN}",
                "Accept": "application/json"
            }

            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()

            org_data = response.json()
            org.name = org_data['name'][:20] + '...' if (
                len(org_data['name']) > 20 and dashboard) else org_data['name']
            org.website = org_data.get('website_url', '')
            org.logo = org_data.get('logo_url', '')
            org.save()
            user_pledge_orgs.append(org)

        except requests.RequestException as e:
            logger.error(f"Failed to fetch organization data for {
                         org.id}: {str(e)}")
            continue

    return user_pledge_orgs


def saveAllUserData(userInfo, userData, userFile):
    try:
        # Reset users custom organizations
        UsersCharityOwnEvent.objects.filter(user=userInfo).delete()

        # Handle profile photo
        if 'profile_photo' in userFile:
            userInfo.profile_photo = userFile['profile_photo']

        # Update user info
        fullname = userData.get('fullname', '').strip().split(' ', 1)
        if len(fullname) >= 2:
            userInfo.first_name = fullname[0]
            userInfo.last_name = fullname[1]

        userInfo.state = userData.get('state', '').strip()
        userInfo.city = userData.get('city', '').strip()
        userInfo.about_me = userData.get('about_me', '').strip()
        userInfo.giving_motivation = userData.get('why_i_give', '').strip()
        userInfo.save()

        # Process organizations
        causes = userData.getlist('causes', [])
        skills = userData.getlist('skills', [])
        pledge_organizations = userData.getlist('pledge_organizations[]', [])
        user_organizations = userData.getlist('user_organizations[]', [])

        for org_id in pledge_organizations:
            if org_id.strip():
                PledgeOrganizations.objects.get_or_create(id=org_id.strip())

        for org_name in user_organizations:
            if org_name.strip():
                UsersCharityOwnEvent.objects.create(
                    user=userInfo,
                    name=org_name.strip()
                )

        # Update relations
        new_causes = Causes.objects.filter(id__in=causes)
        new_skills = Skill.objects.filter(id__in=skills)
        new_pledge_orgs = PledgeOrganizations.objects.filter(
            id__in=pledge_organizations
        )

        user_causes = UserCauses.objects.get(user=userInfo)
        user_skills = UserSkills.objects.get(user=userInfo)
        user_pledge_orgs = UsersPledgeOrganizations.objects.get(user=userInfo)

        user_skills.skill.set(new_skills)
        user_causes.cause.set(new_causes)
        user_pledge_orgs.pledge_organization.set(new_pledge_orgs)

        return False  # No error

    except Exception as e:
        logger.error(f"Save user data error: {str(e)}")
        return str(e)


def updatePassword(request, userData, userInfo):
    try:
        password = userData.get('password', '')
        new_password = userData.get('new_password', '')
        confirm_new_password = userData.get('confirm_new_password', '')

        if not userInfo.check_password(password):
            return 'Your old password was entered incorrectly. Please enter it again.'

        if new_password != confirm_new_password:
            return 'Passwords do not match!'

        if len(new_password) < 8 or not all([
            re.search(r'[A-Z]', new_password),
            re.search(r'[a-z]', new_password),
            re.search(r'\d', new_password)
        ]):
            return 'Password must be at least 8 characters long and contain uppercase, lowercase, and numbers.'

        userInfo.set_password(new_password)
        userInfo.save()
        update_session_auth_hash(request, userInfo)
        return False  # No error

    except Exception as e:
        logger.error(f"Update password error: {str(e)}")
        return 'An error occurred while updating your password'
