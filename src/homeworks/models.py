import json
from django.db import models
from django.db.models.functions import Length
from users.models import User, UserProfile
from django.contrib.staticfiles import finders
from django.conf import settings
from .validators import validate_image
from .utils import (
	time_to_string,
	upload_location,
	upload_book,
	create_grades,
	)


class Grade(models.Model):
	grade = models.IntegerField(choices=create_grades(), unique=True, default=10)

	def __str__(self):
		return str(self.grade)


class Subject(models.Model):
	name = models.CharField(max_length=15)
	full_name = models.CharField(max_length=25)
	grade = models.ForeignKey(Grade, related_name='subjects', on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Book(models.Model):
	name = models.CharField(max_length=20)
	full_name = models.CharField(max_length=35)
	slug = models.SlugField(max_length=10)
	subject = models.ForeignKey(Subject, related_name='books', on_delete=models.CASCADE)
	image = models.ImageField(upload_to=upload_book, null=True, blank=True)
	number_list = models.CharField(max_length=10000, default='')
	type_list = models.CharField(max_length=1000, default='')

	@property
	def numbers(self):
		return json.loads(self.number_list)

	@property
	def types(self):
		if self.type_list:
			return json.loads(self.type_list)
		else:
			return None

	@property
	def number_dict(self):
		N = self.numbers
		T = self.types
		D = {}
		if not T:
			return {}
		for val, _ in T:
			A = list(filter(lambda x: val in x, N))
			typenumbers = map(lambda z: z[len(val):],filter(lambda x: val in x, N))
			D[val] = list(typenumbers)
		return D

	def set_numbers(self, N):
		self.number_list = json.dumps(N)

	def set_types(self, T):
		self.type_list = json.dumps(T)

	def __str__(self):
		return self.name


class HomeworkQuerySet(models.query.QuerySet):
	# Filter
	def number(self, num):
		return self.filter(
			number__exact = num)

	def publisher(self, user):
		return self.filter(
			publisher__exact = user)

	# Order
	def date(self):
		return self.order_by('-publication_date')

	def likes(self):
		return sorted(self, key=lambda x: x.likes.count(), reverse=True)

	def dislikes(self):
		return sorted(self, key=lambda x: x.dislikes.count(), reverse=True)
		

class HomeworkManager(models.Manager):
	def get_queryset(self):
		return HomeworkQuerySet(self.model, using=self._db)

	def create_homework(self, grade, subject, book, number, images, user_id):
		user = User.objects.all().get(id=user_id)
		publisher_profile = UserProfile.objects.get(user=user)
		grade = Grade.objects.all().get(id=grade)
		subject = grade.subjects.get(id=subject)
		book = subject.books.get(id=book)
		homework = self.create(publisher=user,
			publisher_profile=publisher_profile,
			grade=grade,
			subject=subject,
			book=book,
			number=number)
		for i in range(len(images)):
			hwimage = HomeworkImage.objects.create(
				homework=homework, 
				image=images[i],
				index=i)
			try:
				hwimage.full_clean()
			except:
				homework.delete()
				raise
			hwimage.save()
		homework.save()
		return homework


class Homework(models.Model):
	publisher = models.ForeignKey(User, related_name='homeworks', on_delete=models.CASCADE, null=True)
	publisher_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	grade = models.ForeignKey(Grade, related_name='homeworks', on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, related_name='homeworks', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, related_name='homeworks', on_delete=models.CASCADE)
	number = models.CharField(max_length=15)

	publication_date = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

	@property
	def uploaded(self):
		return time_to_string(self.publication_date)

	@property
	def num(self):
		return f"{self.paragraph}.{self.number}"

	objects = HomeworkManager()

	def __str__(self):
		return f'{self.book}-{self.number}({self.publisher.username})'


class HomeworkImage(models.Model):
	homework = models.ForeignKey(Homework, related_name='images', on_delete=models.CASCADE)
	image = models.ImageField(upload_to=upload_location, validators=[validate_image], null=True, blank=True)
	index = models.IntegerField(default=0)

	def __str__(self):
		s = f'{self.homework.book}-{self.homework.number}'
		s1 = f'({self.homework.publisher.username})'
		s2 = f' Image {self.index}'
		return s + s1 + s2


class New(models.Model):
	publisher = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)
	summary = models.CharField(max_length=40)
	description = models.CharField(max_length=400)
	publication_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.summary)