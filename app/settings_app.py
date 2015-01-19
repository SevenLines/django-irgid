

INSTALLED_APPS = (

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'cms',  # django CMS itself
    'mptt',
    'treebeard',  # utilities for implementing a tree using materialised paths
    'menus',  # helper for model independent hierarchical website navigation
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
    'textpage',
)

# THUMBNAIL_DEBUG = True
