from django.shortcuts import render
from rest_framework import viewsets
from users.models import User, UserProfile
from .serializers import (
	GradeSerializer,
	SubjectSerializer,
	BookSerializer,
	HomeworkSerializer,
	HomeworkImageSerializer,
	UserSerializer,
	UserProfileSerializer)
from homeworks.models import (
	Grade,
	Subject,
	Book,
	Homework,
	HomeworkImage)

# Create your views here.

class GradesView(viewsets.ModelViewSet):
	queryset = Grade.objects.all()
	serializer_class = GradeSerializer

class SubjectsView(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = SubjectSerializer

class BooksView(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer

class HomeworksView(viewsets.ModelViewSet):
	queryset = Homework.objects.all()
	serializer_class = HomeworkSerializer

class UsersView(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserProfilesView(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer