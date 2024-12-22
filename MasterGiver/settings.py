"""
Django settings for MasterGiver project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')


# Load environment variables
env_path = BASE_DIR / 'apis.env'
load_dotenv(env_path)

# SECURITY SETTINGS
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-default-secret-key')
# Default to False in production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'mastergiver-e5f12f89fc67.herokuapp.com',
    'www.mastergiver.com',
    'mastergiver.com'
]

# Application definition
INSTALLED_APPS = [
    'organizations',
    'causes',
    'debug_toolbar',
    'corsheaders',
    'givers',
    'mailerlite_integration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
]

# MIDDLEWARE SETTINGS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Make sure it's right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# URL AND TEMPLATE SETTINGS
ROOT_URLCONF = 'MasterGiver.urls'
WSGI_APPLICATION = 'MasterGiver.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# DATABASE SETTINGS
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# AUTHENTICATION SETTINGS
AUTH_USER_MODEL = 'givers.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'MasterGiver.authentication.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'givers.validators.PasswordStrengthValidator',
    },
]

# STATIC FILES SETTINGS
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise Settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_MAX_AGE = 31536000

# MEDIA FILES SETTINGS
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File Upload Settings
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# CORS SETTINGS
CORS_ALLOWED_ORIGINS = [
    f"http://{host}" for host in ALLOWED_HOSTS
] + [f"https://{host}" for host in ALLOWED_HOSTS]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# INTERNATIONALIZATION SETTINGS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
INTERNAL_IPS = ['127.0.0.1']

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('BREVO_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('BREVO_API_KEY')
DEFAULT_FROM_EMAIL = 'MasterGiver <carlos@mastergiver.com>'
SERVER_EMAIL = 'carlos@mastergiver.com'

# Add this for debugging
EMAIL_DEBUG = True

# For debugging DNS issues
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.core.mail': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.core.mail.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Add SMTP debugging
        'smtp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'smtp.connection': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# CLOUDINARY SETTINGS
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

if not all(CLOUDINARY_STORAGE.values()):
    raise ValueError(
        "CLOUDINARY_CLOUD_NAME, API_KEY and API_SECRET must be set")


# PRODUCTION SETTINGS
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin configuration
ADMINS = [('Admin', os.environ.get('ADMIN_EMAIL', 'admin@mastergiver.com'))]

# API Tokens
PLEDGE_API_TOKEN = os.getenv('PLEDGE_API_TOKEN')


# Mailerlite Integration
MAILERLITE_API_KEY = os.environ.get('MAILERLITE_API_KEY')
if not MAILERLITE_API_KEY:
    raise ValueError("MAILERLITE_API_KEY not found in environment variables")

MAILERLITE_DEFAULT_GROUP_ID = os.environ.get('MAILERLITE_DEFAULT_GROUP_ID')
