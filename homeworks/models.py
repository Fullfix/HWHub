from django.db import models
from users.models import User, UserProfile
from django.contrib.staticfiles import finders
from django.conf import settings
import json
import datetime
import pytz

# Create your models here.
def time_to_string(date):
	timezone = pytz.timezone(settings.TIME_ZONE)
	upload = date.astimezone(timezone)
	now = timezone.localize(datetime.datetime.now())
	d = now - upload
	year = datetime.timedelta(days=365)
	month = datetime.timedelta(days=30)
	week = datetime.timedelta(days=7)
	day = datetime.timedelta(days=1)
	hour = datetime.timedelta(hours=1)
	minute = datetime.timedelta(minutes=1)
	second = datetime.timedelta(seconds=1)
	s = ''
	if d // year:
		s = f'{d // year} год назад'
	elif d // month:
		s = f'{d // month} месяцев назад'
	elif d // week:
		s = f'{d // week} недель назад'
	elif d // day:
		s = f'{d // day} дней назад'
	elif d // hour:
		s = f'{d // hour} часов назад'
	elif d // minute:
		s = f'{d // minute} минут назад'
	elif d // second:
		s = f'{d // second} секунд назад'
	return s

def upload_location(instance, filename):
	return 'uploads/%s/%s.%s.%s.%s' % (instance.publisher.id,
		instance.paragraph,
		instance.number,
		str(datetime.datetime.now()),
		'.'.split(filename)[-1])

def load_books():
	path = finders.find('maths/books.json')
	with open (path, 'r') as f:
		books = json.load(f)
	return books

class HomeworkManager(models.Manager):
	def create_homework(self, params, user):
		publisher_profile = UserProfile.objects.get(user=user)
		homework = self.create(publisher=user,
			publisher_profile=publisher_profile,
			book=params['book'],
			paragraph=params['paragraph'],
			number=params['number'],
			image=params['image'])
		return homework

class Homework(models.Model):
	publisher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	publisher_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	book = models.CharField(choices=load_books()['algebra'], max_length=30)
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

	publication_date = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name='likes', blank=True)
	dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

	@property
	def uploaded(self):
		return time_to_string(self.publication_date)

	objects = HomeworkManager()

	def __str__(self):
		return f'{self.book}-{self.paragraph}-{self.number}({self.publisher.username})'