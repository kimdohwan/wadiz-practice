from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'wadiz.ap-northeast-2.elasticbeanstalk.com',
]

WSGI_APPLICATION = 'config.wsgi.production.application'

SECRET_KEY = secrets['SECRET_KEY']
