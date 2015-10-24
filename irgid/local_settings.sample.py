DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'irgid',
        'PASSWORD': '12345',
        'USER': 'mk',
        'HOST': 'localhost',
    }
}

SECRET_KEY = "*=xv5*k(d=qd$ds+pyhvsa4qlpvj9413j!si2r5y9%-q3t+84p"
DEBUG = True
DONT_USE_METRICS = True

ALLOWED_HOSTS = [
    "*"
]
