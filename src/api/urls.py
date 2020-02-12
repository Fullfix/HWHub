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

urlpatterns = [
	path('', include(router.urls))
]