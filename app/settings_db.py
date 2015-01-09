from app.settings import credentials

DATABASES = {
    'default': {
        'ENGINE': credentials["database"]['ENGINE'],
        'NAME': credentials["database"]['NAME'],
        'PASSWORD': credentials["database"]['PASSWORD'],
        'USER': credentials["database"]['USER'],
        'HOST': credentials["database"]['HOST'],
        'PORT': credentials["database"]['PORT'],
    }
}

#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'mmailm_irgid11',  # Or path to database file if using sqlite3.
#         # The following settings are not used with sqlite3:
#         'USER': 'mmailm_irgid11',
#         'PASSWORD': '39ZFeWtVT3',
#         'HOST': 'postgresql2.locum.ru',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': '',  # Set to empty string for default.
#     }
# }