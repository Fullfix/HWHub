from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def upload_location(instance, filename):
	return 'uploads/%s/%s.%s.%s' % (instance.publisher.id, 
		instance.paragraph, 
		instance.number,
		'.'.split(filename)[-1])

class HomeworkManager(models.Manager):
	def create_homework(self, params, user):
		homework = self.create(publisher=user,
			book=params['book'],
			paragraph=params['paragraph'],
			number=params['number'],
			image=params['image'])
		return homework

class Homework(models.Model):
	publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	book = models.CharField(max_length=30)
	paragraph = models.IntegerField()
	number = models.IntegerField()
	image = models.ImageField(upload_to=upload_location,
		null=True,
		blank=True,
		width_field='width_field',
		height_field='height_field',
		)
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)

	objects = HomeworkManager()