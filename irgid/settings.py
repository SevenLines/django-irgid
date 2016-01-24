# coding=utf-8
"""
Django settings for irgid project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Application definition
TESTING= 'test' in sys.argv

INSTALLED_APPS = (
    'djangocms_admin_style',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'sekizai',  # for javascript and css management
    'filer',
    'easy_thumbnails',
    'django_extensions',

    'excursions',
    'django_assets',
    'ex_tags',
    'utils',
    'request',
    'sharedcontroll',
    'custom_settings',
    'debug_toolbar',
    'simple_history',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

ROOT_URLCONF = 'irgid.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.core.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'irgid.context_processors.debug',
                'irgid.context_processors.custom_settings',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

WSGI_APPLICATION = 'irgid.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Irkutsk'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "templates/static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_FUNCTION': "irgid.utils.cache_key",
        'KEY_PREFIX': '0957c690-7ddb-49fb-80e1-890def9f484b',
    }
}



if TESTING:
    class DisableMigrations(object):
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return "notmigrations"
    DEBUG = False
    TEMPLATE_DEBUG = False
    MIGRATION_MODULES = DisableMigrations()

try:
    from local_settings import *
except:
    print("Failed to import settings, local_settings.py don't exists or incorretc")
    exit()

# -=-=-=-=-=-=-=-=-=-=-=-=-
# APPLICATION SETTINGS BEGIN
def travel_menu_item_visible(context):
    from excursions.models import Excursion, ExcursionCategory
    if context['user'].is_authenticated():
        return True
    return Excursion.objects.filter(
        published=True,
        category_id=ExcursionCategory.objects.get_travel_id()
    ).exists()

MENU = [
    ('index', u'Экскурсии', '^/excursions|^$|^/$', '', lambda c: True),
    ('calendar', u'Календарь Экскурсий', '^/calendar', '', lambda c: True),
    ('travel:index', u'Путешествия', '^/travel', '', travel_menu_item_visible),
    ('about', u'О нас', '^/about', '', lambda c: True),
    ('faq', u'Частые вопросы (FAQ)', '^/faq', '', lambda c: True),
    ('gallery:index', u'Галерея', '^/gallery', '', lambda c: True),
    ('settings', u'Настройки', '^/settings', '', lambda c: c['user'].is_authenticated()),
]

CUSTOM_SETTINGS = {
    'phone': (u'Телефон', '', 'String'),
    'email': (u'Электронная почта', '', 'String'),
    'headers_excursions': (u'Заголовоки для экскурсий', 'Кол-во человек в группе/Цена/Взрослый/Детский/Дошкольный', 'String'),
    'headers_travel': (u'Заголовоки для путуешествий', 'Кол-во человек в группе/Цена/Эконом/Стандарт/Люкс', 'String'),
    'copyright': (u'Копирайт', """© 2015 Экскурсионное агентство «<span itemprop="author" itemscope itemtype="http://schema.org/Person"><span itemprop="name">Иргид</span></span>».<br>Все права защищены.""", 'String'),

    'about': (u'О нас', '', 'String'),
    'faq': (u'FAQ', '', 'String'),
    'calendar': (u'Расписание экскурсий', '', 'String'),

    'excuse_for_not_exists': (u'Извинение', "<h2 style='text-align: center;'>Этот раздел сейчас в разработке</h2>", 'String'),

    'gallery_id': (u'Раздел "Галерея"', None, 'ForeignKey', 'excursions.ExcursionCategory:title'),
    'travel_id': (u'Раздел "Путешествия"', None, 'ForeignKey', 'excursions.ExcursionCategory:title'),

    'email_for_appointments': (u"Почта для перенаправления заявок", '', 'String'),
}

ASSETS_MODULES = [
    'irgid.assets'
]

THUMBNAIL_DEBUG = False
if not DEBUG:
    ASSETS_CACHE = False
    ASSETS_MANIFEST = False
    ASSETS_AUTO_BUILD = False

ASSETS_ROOT = os.path.join(BASE_DIR, 'templates/static')
DONT_USE_METRICS = False

MONTHS = [
    (1, 'Январь'),
    (2, 'Февраль'),
    (3, 'Март'),
    (4, 'Апрель'),
    (5, 'Май'),
    (6, 'Июнь'),
    (7, 'Июль'),
    (8, 'Август'),
    (9, 'Сентябрь'),
    (10, 'Октябрь'),
    (11, 'Ноябрь'),
    (12, 'Декабрь'),
]
