from .base import *

ALLOWED_HOSTS = ['13.124.216.96']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': SECRET_KEY.get('DATABASE_PASSWORD'),
        'HOST': 'ls-7da01be2e60209c7f8c0b9a8bd3ec84b15f343c0.cuiyonyqrp2z.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}