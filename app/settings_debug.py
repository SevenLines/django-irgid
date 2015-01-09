from app.settings import credentials

DEBUG = credentials['DEBUG']
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = credentials['ALLOWED_HOSTS']
