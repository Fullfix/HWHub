from django.urls import path
from . import views

urlpatterns = [
	path('', views.books, name='books'),
	path('algebra/<str:book>/<int:p>/<int:num>', views.get_hw, name='algebra'),
	path('algebra/upload', views.upload_hw, name='upload'),
]