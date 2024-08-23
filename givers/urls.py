from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('what-care-about/', views.what_care_about, name='what_care_about'),
    path('api/organizations', views.fetch_organizations,
         name='fetch_organizations'),
    path('preview-profile/', views.preview_profile, name='preview_profile'),
]
