from rest_framework import serializers
from users.models import User, UserProfile
from homeworks.models import (
	Grade,
	Subject,
	Book,
	Homework,
	HomeworkImage)

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'url', 'username', 'admin', 'staff', 'profile']

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserProfile
		fields = ['id', 'url', 'user', 'name', 'surname', 'grade', 'photo']

class SubjectSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Subject
		fields = ['id', 'url', 'name', 'full_name', 'grade', 'books']

class BookSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Book
		fields = ['id', 'url', 'name', 'slug', 'full_name', 'image', 'subject', 'number_list']

class GradeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		subjects = SubjectSerializer(many=True, read_only=True)
		model = Grade
		fields = ['id', 'url', 'grade', 'subjects']

class HomeworkSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Homework
		fields = ['id', 'url', 'publisher', 'grade', 'subject',
		'book', 'number', 'publication_date', 'likes', 'dislikes']

class HomeworkImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = HomeworkImage
		fields = '__all__'