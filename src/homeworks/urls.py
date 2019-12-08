from django.urls import path
from . import views

urlpatterns = [
	path('', views.books, name='books'),
	path('<str:subject>/<str:book>/<int:p>/<int:num>', views.GetHW.as_view(), name='algebra'),
	path('upload/', views.UploadHW.as_view(), name='upload'),
	path('like/', views.LikeHW.as_view(), name='like_hw'),
	path('dislike/', views.DislikeHW.as_view(), name='dislike_hw'),
	path('get_opinion/', views.GetHWOpinion.as_view(), name='get_opinion'),
	path('get_json_books/', views.get_json_books, name='get_json_books'),
	path('get_json_numbers/', views.get_json_numbers, name='get_json_numbers'),
]