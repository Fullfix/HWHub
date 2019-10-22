from django.urls import path
from . import views

urlpatterns = [
	path('', views.books, name='books'),
	path('algebra/<str:book>/<int:p>/<int:num>', views.get_hw, name='algebra'),
	path('algebra/upload', views.UploadHW.as_view(), name='upload'),
	path('like/', views.LikeHW.as_view(), name='like_hw'),
	path('dislike/', views.DislikeHW.as_view(), name='dislike_hw'),
	path('get_opinion/', views.GetHWOpinion.as_view(), name='get_opinion')
]