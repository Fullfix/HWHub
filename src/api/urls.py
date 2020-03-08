from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('grades', views.GradesView)
router.register('subjects', views.SubjectsView)
router.register('books', views.BooksView)
router.register('homeworks', views.HomeworksView)
router.register('users', views.UsersView)
router.register('profiles', views.UserProfilesView)
# router.register('create', views.CreateHomeworkView, basename="Homework")

urlpatterns = [
	path('', include(router.urls)),
	path('get_user_id/', views.GetUserId.as_view()),
	path('update_profile/<int:pk>', views.ProfileUpdateAPIView.as_view()),
	path('update_username/<int:pk>', views.UserNameUpdateAPIView.as_view()),
	path('create_homework', views.CreateHomeworkAPIView.as_view()),
]