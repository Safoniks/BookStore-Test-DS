print('Example settings')

SECRET_KEY = 'YOUR_SECURITY_KEY'
DEBUG = True

HOST = 'YOUR_IP'  # host IP or Name
ALLOWED_HOSTS = [HOST]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'password',
        'HOST': 'db_host',
        'PORT': 'db_port',
    }
}
