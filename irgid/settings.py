# coding=utf-8
# Django settings for adpp project.

import os
import json

import sys

gettext = lambda s: s
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))

try:
    credentials_path = ""
    credentials_path = os.path.join(PROJECT_PATH, "credentials.json")
    credentials = json.load(open(credentials_path))
except IOError as e:
    print("check existance of %s" % credentials_path)
    raise e

try:
    from settings_debug import *
except ImportError:
    pass

try:
    from settings_db import *
except ImportError:
    pass

try:
    from settings_app import *
except ImportError:
    pass


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Irkutsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ru', 'Russian')
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates/static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = credentials['SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'request.middleware.RequestMiddleware',
)

ROOT_URLCONF = 'irgid.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'irgid.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

CMS_TEMPLATES = (
    ('_/base.html', "base"),
)

MIGRATION_MODULES = {
    # 'cms': 'cms.migrations_django',
    'filer': 'filer.migrations_django',
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'irgid.context_processors.debug',
    'sekizai.context_processors.sekizai',
)

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

ASSETS_MODULES = [
    'irgid.assets'
]

THUMBNAIL_DEBUG = False

if not DEBUG:
    ASSETS_CACHE = False
    ASSETS_MANIFEST = False
    ASSETS_AUTO_BUILD = False

ASSETS_ROOT = os.path.join(PROJECT_PATH, 'templates/static')
DONT_USE_METRICS = False

EMAIL_HOST = 'smtp.locum.ru'
EMAIL_HOST_USER = 'robot@irgid.ru'
EMAIL_HOST_PASSWORD = 'I_YzdH-FM2(f'
EMAIL_TIMEOUT = 30

MENU = [
    ('index', u'Экскурсии', '^/excursions|^$|^/$'),
    ('about', u'О нас', '^/about'),
    ('faq', u'FAQ', '^/faq'),
    ('gallery:index', u'Галерея', '^/gallery'),
]