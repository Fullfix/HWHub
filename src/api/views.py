from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import exceptions
from users.models import User, UserProfile
from . import serializers
from homeworks.models import (
	Grade,
	Subject,
	Book,
	Homework,
	HomeworkImage)
from .permissions import IsAdminOrReadOnly, UserIsOwnerOrReadOnly, UserIsOwnerOrReadOnlyProfile

# Create your views here.

class GradesView(viewsets.ModelViewSet):
	queryset = Grade.objects.all()
	serializer_class = serializers.GradeSerializer

class SubjectsView(viewsets.ModelViewSet):
	queryset = Subject.objects.all()
	serializer_class = serializers.SubjectSerializer

class BooksView(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = serializers.BookSerializer

class HomeworksView(viewsets.ModelViewSet):
	queryset = Homework.objects.all()
	serializer_class = serializers.HomeworkSerializer

class UsersView(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer

class UserProfilesView(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = serializers.UserProfileSerializer

class ProfileUpdateAPIView(generics.RetrieveAPIView,
                               mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnlyProfile,
    )
    serializer_class = serializers.ProfileUpdateSerializer

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs['pk']).profile
        return obj

    def post(self, request, *args, **kwargs):
        print(request.data)
        return self.update(request, *args, **kwargs)


class UserNameUpdateAPIView(generics.RetrieveAPIView,
	mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = serializers.UserNameUpdateSerializer
    model = User

    def get_object(self):
        obj = get_object_or_404(User, pk=self.kwargs['pk'])
        return obj

    def put(self, request, *args, **kwargs):
    	user = User.objects.all().get(pk=kwargs['pk'])
    	if not user.check_password(request.data.get('password')):
    		return Response({"error":"passwords dont match"})
    	return self.update(request, *args, **kwargs)


class CreateHomeworkAPIView(generics.CreateAPIView):
	serializer_class = serializers.HomeworkCreateSerializer
	permission_classes = (
		permissions.IsAuthenticated,
		)

	def perform_create(self):
		serializer.save(user=self.request.user)

class GetUserId(APIView):
	renderer_classes = [JSONRenderer]

	def get(self, request):
		return Response(request.user.id)