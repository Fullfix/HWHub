"""
WSGI config for HWHUB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/fullfix/Documents/HWHub/src')

sys.path.append('/home/fullfix/Documents/HWHub/LinuxLib/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'HWHUB.settings.dev'

application = get_wsgi_application()
