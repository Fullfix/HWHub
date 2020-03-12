from rest_framework import serializers, status
from users.models import User, UserProfile
from rest_framework.response import Response
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

class ModelListField(serializers.ListField):
	def to_representation(self, data):
		return [self.child.to_representation(item) if item is not None else None for item in data]

class HomeworkCreateSerializer(serializers.ModelSerializer):
	images = ModelListField(child=serializers.FileField(max_length=100000, use_url=False))
	class Meta:
		model = Homework
		fields = ['grade', 'subject', 'book', 'number', 'images']


class ProfileUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('pk', 'name', 'surname', 'grade', 'photo')
		extra_kwargs = {'grade': {'required': False}, 'photo': {'required': False}}

	def update(self, instance, validated_data):
		instance.name = validated_data.get("name", instance.name)
		instance.surname = validated_data.get("surname", instance.surname)
		instance.grade = validated_data.get("grade", instance.grade)
		instance.photo = validated_data.get("photo", instance.photo)
		instance.save()
		return instance


class UserNameUpdateSerializer(serializers.ModelSerializer):
	pk = serializers.CharField(read_only=True)
	password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Подтвердите свой пароль',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

	class Meta:
		model = User
		fields = ('pk', 'username', 'password')

	def update(self, instance, validated_data):
		errors = dict()
		instance.username = validated_data.get("username", instance.username)
		instance.save()
		return instance