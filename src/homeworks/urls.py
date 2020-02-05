from django.urls import path
from . import views

urlpatterns = [
	path('<int:grade>/', views.ClassPage.as_view(), name='classpage'),
	path('<int:grade>/<str:subject>/<str:book>/<int:par>/<int:num>',
	 views.BookPage.as_view(), name='bookpage'),
	path('<int:grade>/<str:subject>/<str:book>', views.GrandBookPage.as_view(), name='grandbookpage'),
	path('upload/', views.UploadHW.as_view(), name='upload'),
	path('like/', views.LikeHW.as_view(), name='like_hw'),
	path('dislike/', views.DislikeHW.as_view(), name='dislike_hw'),
	path('get_opinion/', views.GetHWOpinion.as_view(), name='get_opinion'),
	path('get_json_file', views.get_json_file, name='json_file'),
	path('redirect_hw/<str:number>/<path:path>', views.redirect_hw, name='redirect_hw'),
]