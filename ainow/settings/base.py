"""
Django settings for ainow project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import yaml
from .paths import *

config = yaml.load(open(os.path.join(PROJECT_ROOT, 'conf', 'general.yml')))

DEBUG = bool(int(config.get('STAGING')))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('AINOW_DB_NAME'),
        'USER': config.get('AINOW_DB_USER'),
        'PASSWORD': config.get('AINOW_DB_PASS'),
        'HOST': config.get('AINOW_DB_HOST'),
        'PORT': config.get('AINOW_DB_PORT'),
    }
}

SECRET_KEY = config.get('DJANGO_SECRET_KEY')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'pipeline',
    'sorl.thumbnail',
    'markitup',
    'account',
    'autoslug',
    'adminsortable2',

    'ainow',  # Base app has management commands so has to be in here
    'conference',
    'faq',
    'pages',
    'blocks',
    'themes'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware'
]

ROOT_URLCONF = 'ainow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
                'ainow.context_processors.add_settings',
                'ainow.context_processors.add_schedule',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'ainow.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Enable email-based login rather than username-based
AUTHENTICATION_BACKENDS = [
    'account.auth_backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PARENT_DIR, 'collected_static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'web'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# Django-Pipeline configuration
# https://django-pipeline.readthedocs.io/en/latest/configuration.html
PIPELINE = {
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
                'sass/main.scss',
            ),
            'output_filename': 'css/main.css',
        },
    },
    'JAVASCRIPT': {
        'app': {
            'source_filenames': (
                'javascripts/jquery.js',
                'javascripts/bootstrap.js',
                'javascripts/js.cookie.js',
                'conference/javascripts/profile-photo.js',
            ),
            'output_filename': 'javascripts/scripts.js',
        },
    },
    'CSS_COMPRESSOR': 'django_pipeline_csscompressor.CssCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.slimit.SlimItCompressor',
    'DISABLE_WRAPPER': True,
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
    ),
    # Use the libsass commandline tool (that's bundled with libsass) as our
    # sass compiler, so there's no need to install anything else.
    'SASS_BINARY': os.path.join(PARENT_DIR, 'virtualenv-ainow', 'bin', 'sassc')
}


# Uploaded files

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PARENT_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'


# Logging

# Log WARN and above to stderr; ERROR and above by email when DEBUG is False.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
        },
        'debug_console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins', 'console'],
            'level': 'WARN',
            'propagate': True,
        },
        # To see all of the database statements being executed in your terminal
        # uncomment the following (DEBUG must be True too)
        # 'django.db.backends': {
        #     'handlers': ['debug_console'],
        #     'level': 'DEBUG',
        #     'propagate': True,
        # },
    }
}


# Cookies

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False  # We need this for the markdown ajax preview


# Allowed hosts

ALLOWED_HOSTS = config.get('ALLOWED_HOSTS', [])


# Django sites
SITE_ID = 1
SITE_BASE_URL = config.get('SITE_BASE_URL', '')
SITE_NAME = config.get('SITE_NAME', 'MapIt')


# Use mailcatcher in development?
USE_MAILCATCHER = config.get('USE_MAILCATCHER', False)
if USE_MAILCATCHER:
    EMAIL_HOST = '127.0.0.1'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

# MarkItUp settings
MARKITUP_FILTER = ('conference.utils.bleached_markdown', {})
MARKITUP_SET = 'markitup/sets/markdown/'


# Bleach settings (used by conference.utils.bleached_markdown)
BLEACH_ALLOWED_TAGS = [
    u'a',
    u'abbr',
    u'acronym',
    u'b',
    u'blockquote',
    u'code',
    u'em',
    u'i',
    u'li',
    u'ol',
    u'strong',
    u'ul',
    # We've added these:
    u'p',
    u'img',
    u'pre',
    u'h2',
    u'h3',
    u'h4',
    u'h5',
    u'h6',
]

BLEACH_ALLOWED_ATTRIBUTES = {
    u'a': [u'href', u'title'],
    u'acronym': [u'title'],
    u'abbr': [u'title'],
    # We've added these:
    u'img':  [u'src', u'alt', u'title'],
}


# Django user accounts settings
ACCOUNT_OPEN_SIGNUP = False  # You have to be invited
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
CONTACT_EMAIL = config.get('CONTACT_EMAIL', '')
DEFAULT_FROM_EMAIL = CONTACT_EMAIL
ACCOUNT_USER_DISPLAY = lambda user: user.email
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'account_login'


# mySociety-specific settings
GOOGLE_ANALYTICS_ACCOUNT = config.get('GOOGLE_ANALYTICS_ACCOUNT')
