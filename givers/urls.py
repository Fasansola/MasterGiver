from django.urls import path
from django.contrib.auth import views as auth_views

from django.contrib.sitemaps import views as sitemap_views
from .sitemaps import StaticViewSitemap, UserSitemap

from . import views

sitemaps = {
    'static': StaticViewSitemap,
    'profiles': UserSitemap,
}


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name="about"),
    path('faq', views.faq, name="faq"),
    path('terms', views.terms, name="terms"),
    path('privacy', views.privacy, name="privacy"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-setup/', views.what_care_about, name='what_care_about'),
    path('api/organizations', views.fetch_organizations,
         name='fetch_organizations'),
    path('preview-profile/', views.preview_profile, name='preview_profile'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password', views.change_password, name='change_password'),
    path('clear-profile-picture/', views.clear_profile_picture,
         name='clear_profile_picture'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
