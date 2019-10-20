from django.urls import path
from . import views

urlpatterns = [
	path('', views.books, name='books'),
	path('algebra/<str:book>/<int:p>/<int:num>', views.get_hw, name='algebra'),
	path('algebra/upload', views.upload_hw, name='upload'),
	path('like/', views.like_hw, name='like_hw'),
	path('dislike/', views.dislike_hw, name='dislike_hw')
]