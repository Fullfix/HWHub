from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
	)
from django.core.validators import MinValueValidator, MaxValueValidator
# from .forms import create_grades

# Create your models here.
def upload_location(instance, filename):
	return 'users/%s/profile.%s' % (instance.user.id, '.'.split(filename)[-1])

def create_grades():
	C = []
	for i in range(1, 12):
		C.append((i, str(i)))
	return tuple(C)

class UserManager(BaseUserManager):
	def create_user(self, username, password=None, is_admin=False, is_staff=False):
		if not username:
			raise ValueError('Отсутствует имя пользователя')
		if not password:
			raise ValueError('Отсутствует пароль')

		user_obj = self.model(username=username)
		user_obj.set_password(password)
		user_obj.admin = is_admin
		user_obj.staff = is_staff
		user_obj.save(using=self._db)
		return user_obj

	def create_superuser(self, username, password=None):
		user = self.create_user(
			username=username,
			password=password,
			is_admin=True,
			is_staff=True
			)
		return user

	def create_staffuser(self, username, password=None):
		user = self.create_user(
			username=username,
			password=password,
			is_staff=True
			)
		return user


class User(AbstractBaseUser):
	username = models.CharField(max_length=20, unique=True)
	admin = models.BooleanField(default=False)
	staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'

	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property	
	def is_admin(self):
		return self.admin

	@property
	def is_staff(self):
		return self.staff


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=15)
	surname = models.CharField(max_length=15)
	grade = models.IntegerField(choices=create_grades(), default=10)
	photo = models.ImageField(upload_to=upload_location, default='users/default.jpg')

	def __str__(self):
		return f"{self.user.username}'s Profile"