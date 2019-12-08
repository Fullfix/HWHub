from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import UserRegisterForm
from .models import UserProfile, User
from homeworks.models import Homework

def index(request):
	return render(request, 'users/index.html')

class RegisterView(View):
	form_class = UserRegisterForm
	template_name = 'registration/register.html'

	def get(self, request):
		form = self.form_class()
		context = {'form': form}
		return render(request, self.template_name, context)

	def post(self, request):
		print(request.POST)
		form = self.form_class(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			name = form.cleaned_data['name']
			surname = form.cleaned_data['surname']
			grade = form.cleaned_data['grade']
			new_user = User.objects.create_user(username=username, password=password)
			new_user.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			profile = UserProfile(user=user, name=name, surname=surname, grade=grade)
			profile.save()
			login(request, user)
			return redirect('index')

def profile(request, id_):
	user = User.objects.filter(id=id_).first()
	profile = UserProfile.objects.filter(user=request.user)[0]
	homeworks = Homework.objects.all().publisher(user)
	context = {'user':request.user, 'profile':profile, 'homeworks':homeworks}
	return render(request, 'users/profile.html', context)

def navbar(request):
	profile = UserProfile.objects.filter(user=request.user)[0]
	context = {'user':request.user, 'profile':profile}
	return render(request, 'navbar.html', context)