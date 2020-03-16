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

ADMINS = [('Nikita', 'nbreskanu73@gmail.com')]

SERVER_EMAIL = 'hwhub.inc@bk.ru'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'hwhub.inc@bk.ru'
EMAIL_HOST_PASSWORD = 'FiveNights'
EMAIL_USE_TSL = False
EMAIL_USE_SSL = True