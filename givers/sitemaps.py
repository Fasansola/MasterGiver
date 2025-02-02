# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# If you're using the default User model
from .models import User


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        # Add all your static pages
        return ['home', 'about', 'faq', 'terms', 'privacy', 'signup', 'login']

    def location(self, item):
        return reverse(item)


class UserSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return User.objects.filter(is_active=True)

    def location(self, obj):
        # Make sure this matches your URL pattern
        return reverse('profile', args=[obj.username])

# The rest of your URLs and settings remain the same
