from .base import *
from decouple import config
import os
from datetime import timedelta
import pymysql
pymysql.install_as_MySQLdb()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y(jg#8^pntjid441v#m1%pi(xy&qz7*62&9bgzew280*=gc@=y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(
    BASE_DIR, "/home/pujanraj/boudhhafitness.com/media/")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, "/home/pujanraj/boudhhafitness.com/")


ALLOWED_HOSTS = [
    "*"
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

d_name = config('d_name', default='pujanraj_boudhafitness')
d_user = config('d_user', default='pujanraj_boudhafitness')
d_password = config('d_password', default='boudhafitness')
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
