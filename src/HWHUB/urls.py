"""HWHUB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import handler404
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView
from django.views.i18n import JavaScriptCatalog
from .settings import base
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.MainPage.as_view(), name='main'),
    path('', include('users.urls')),
    path('api/', include('api.urls')),
    path('homework/', include('homeworks.urls')),
    path('', views.LandingPage.as_view(), name='landing'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)

handler404 = views.handler404
handler500 = views.handler500
handler403 = views.handler403