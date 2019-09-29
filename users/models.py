from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .forms import create_grades

# Create your models here.

def upload_location(instance, filename):
	return 'users/%s/profile.%s' % (instance.user.id, '.'.split(filename)[-1])


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=20)
	name = models.CharField(max_length=15)
	surname = models.CharField(max_length=15)
	grade = models.IntegerField(choices=create_grades(), default=10)
	photo = models.ImageField(upload_to=upload_location, null=True, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'