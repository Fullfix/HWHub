from HWHUB.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['breskanun.beget.tech']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hwhub',
        'USER': 'fullfix',
        'PASSWORD': 'FiveNights1987%',
        'HOST': 'hwhub.com',
        'PORT': '',
    }
}