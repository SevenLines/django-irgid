

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'sekizai',  # for javascript and css management
    'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'django.contrib.admin',
    'filer',
    'easy_thumbnails',

    'excursions',
    'django_assets',
    'setup_irgid',
    'ex_tags',
    'utils',
    'request',
    'sharedcontroll',
    'custom_settings',
)

# THUMBNAIL_DEBUG = True
