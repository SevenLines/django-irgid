DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'irgid3',  # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
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