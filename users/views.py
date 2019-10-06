from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from .models import UserProfile

def index(request):
	return render(request, 'users/index.html')

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			profile = UserProfile(user=user, username=username,
				name=form.cleaned_data['name'],
				surname=form.cleaned_data['surname'],
				grade=form.cleaned_data['grade'])
			profile.save()
			login(request, user)
			return redirect('index')

	else:
		form = UserRegisterForm()

	context = {'form': form}
	return render(request, 'registration/register.html', context)

def profile(request, id_):
	user = User.objects.filter(id=id_).first()
	profile = UserProfile.objects.filter(user=request.user)[0]
	context = {'user':request.user, 'profile':profile}
	return render(request, 'users/profile.html', context)


def navbar(request):
	profile = UserProfile.objects.filter(user=request.user)[0]
	context = {'user':request.user, 'profile':profile}
	return render(request, 'navbar.html', context)