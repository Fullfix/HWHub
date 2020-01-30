from django.db import models
from django.db.models.functions import Length
from users.models import User, UserProfile
from django.contrib.staticfiles import finders
from django.conf import settings
from .utils import (
	time_to_string,
	upload_location,
	create_grades,
	)


class HomeworkQuerySet(models.query.QuerySet):
	# Filter
	def number(self, grade, subject, book, p, num):
		return self.filter(
			grade__exact = grade,
			subject__exact = subject,
			book__exact = book, 
			paragraph__exact = int(p),
			number__exact = int(num))

	def publisher(self, user):
		return self.filter(
			publisher__exact = user)

	# Order
	def date(self):
		return self.order_by('-publication_date')

	def likes(self):
		return self.order_by(Length('likes').asc())

	def dislikes(self):
		return self.order_by(Length('dislikes').asc())


class HomeworkManager(models.Manager):
	def get_queryset(self):
		return HomeworkQuerySet(self.model, using=self._db)

	def create_homework(self, params, images, user):
		publisher_profile = UserProfile.objects.get(user=user)
		homework = self.create(publisher=user,
			publisher_profile=publisher_profile,
			grade=params['grade'],
			subject=params['subject'],
			book=params['book'],
			paragraph=params['paragraph'],
			number=params['number'])
		for i, name in enumerate(images.keys()):
			hwimage = HomeworkImage.objects.create(
				homework=homework, 
				image=images[name],
				index=i)
			hwimage.save()
		homework.save()
		return homework

class Homework(models.Model):
	publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	publisher_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	grade = models.IntegerField(choices=create_grades(), default=10)
	subject = models.CharField(max_length=20, default='algebra')
	book = models.CharField(max_length=30, default='NoBook')
	paragraph = models.IntegerField(default=0)
	number = models.IntegerField(default=0)

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
		return f'{self.book}-{self.paragraph}-{self.number}({self.publisher.username})'


class HomeworkImage(models.Model):
	homework = models.ForeignKey(Homework, related_name='images', on_delete=models.CASCADE)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True)
	index = models.IntegerField(default=0)

	def __str__(self):
		s = f'{self.homework.book}-{self.homework.paragraph}-{self.homework.number}'
		s1 = f'({self.homework.publisher.username})'
		s2 = f' Image {self.index}'
		return s + s1 + s2