from django.shortcuts import render, get_object_or_404
from django.core import exceptions
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import status
from rest_framework.serializers import ValidationError
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
from .permissions import (
	IsAdminOrReadOnly, UserIsOwnerOrReadOnly, 
	UserIsOwnerOrReadOnlyProfile, UserIsOwnerOrAdminHomework)

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
        obj = self.get_object()
        self.check_object_permissions(request, obj)
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
    	obj = self.get_object()
    	self.check_object_permissions(request, obj)
    	user = User.objects.all().get(pk=kwargs['pk'])
    	if not user.check_password(request.data.get('password')):
    		raise ValidationError({"password":["Пароли не совпадают"]})
    	return self.update(request, *args, **kwargs)


class CreateHomeworkAPIView(APIView):
	serializer_class = serializers.HomeworkCreateSerializer
	permission_classes = (
		permissions.IsAuthenticated,
		)

	def post(self, request, *args, **kwargs):
		data = dict(request.data)
		data.pop('csrfmiddlewaretoken')
		data.pop('fileinput')
		files = []
		for i in range(10):
			if f'file{i}' in data.keys():
				files.append(data.pop(f'file{i}')[0])
		for i in data.keys():
			data[i] = data[i][0]
		if not files:
			return Response({"success":False, 
				"error":"please choose images of your homework"})
		data['images']=files
		serializer = self.serializer_class(data=data)
		if serializer.is_valid(raise_exception=True):
			pass
		try:
			Homework.objects.create_homework(**data, user_id=request.user.id)
		except BaseException as e:
			return Response({"success":False, "error":str(e)})
		return Response({"success":True})

class DeleteHomeworkAPIView(generics.RetrieveDestroyAPIView):
	permission_classes = (
		permissions.IsAuthenticated,
		UserIsOwnerOrAdminHomework,
		)
	serializer_class = serializers.HomeworkDeleteSerializer
	queryset = Homework.objects.all()
	lookup_field = "pk"


class GetUserId(APIView):
	renderer_classes = [JSONRenderer]

	def get(self, request):
		return Response(request.user.id)


class GetBookNumberDict(APIView):
	renderer_classes = [JSONRenderer]

	def get(self, request, pk):
		book = Book.objects.all().get(pk=pk)
		return Response(book.number_dict)