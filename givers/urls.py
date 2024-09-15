from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('what-care-about/', views.what_care_about, name='what_care_about'),
    path('api/organizations', views.fetch_organizations,
         name='fetch_organizations'),
    path('preview-profile/', views.preview_profile, name='preview_profile'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('clear-profile-picture/', views.clear_profile_picture, name='clear_profile_picture'),
]
