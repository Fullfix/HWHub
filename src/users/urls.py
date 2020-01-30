from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('navbar', views.navbar, name='navbar'),
    path('id<int:id_>', views.profile, name='profile'),
]