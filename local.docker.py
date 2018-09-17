
DEBUG = True

SECRET_KEY = 'YOUR_KEY'

HOST = '*'
ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Europe/Kiev'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bookstore',
        'USER': 'bookstore',
        'PASSWORD': 'bookstore',
        'HOST': 'postgres_db',
        'PORT': '5432',
    }
}
