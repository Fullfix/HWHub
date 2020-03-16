from HWHUB.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
ADMINS = [('Nikita', 'nbreskanu73@gmail.com')]

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'hwhub.inc@bk.ru'
EMAIL_HOST_PASSWORD = 'FiveNights'
EMAIL_USE_TSL = False
EMAIL_USE_SSL = True