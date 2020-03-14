from HWHUB.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ['breskanun.beget.tech']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'breskanun_hw',
        'USER': 'breskanun_hw',
        'PASSWORD': 'U6iUHOs%',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/HWHub/static/'
MEDIA_URL = '/HWHub/media/'