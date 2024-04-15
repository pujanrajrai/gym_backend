from .base import *
from decouple import config
import os
from datetime import timedelta
import pymysql
pymysql.install_as_MySQLdb()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kfnx^&g4mxwck4sqq1w@yrw)8kd$#nipwtzj^keigo-2l+208w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

d_name = config('d_name', default='gym')
d_user = config('d_user', default='root')
d_password = config('d_password', default='pujanrajrai09')
d_host = config('d_host', default='127.0.0.1')
d_port = config('d_port', default='3306')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': d_name,
        'USER': d_user,
        'PASSWORD': d_password,
        'HOST': d_host,
        'PORT': d_port,
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
APPEND_SLASH = True
