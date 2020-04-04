from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.utils.translation import get_language
from .forms import UserRegisterForm
from .models import UserProfile, User
from homeworks.models import Homework


class RegisterView(View):
	form_class = UserRegisterForm

	def post(self, request):
		print(get_language())
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
			data = {'success': True, 'error':""}
			return JsonResponse(data)
		else:
			errors = dict(form.errors.items())
			for key in errors.keys():
				errors[key] = (errors[key][0])
			data = {'success': False, 'error':errors}
			return JsonResponse(data)


@login_required
def profile(request, id_):
	user = get_object_or_404(User, id=id_)
	profile = user.profile
	homeworks = Homework.objects.all().publisher(user)
	context = {'user':request.user, 'page_user':user, 'profile':profile, 'homeworks':homeworks}
	return render(request, 'users/profile.html', context)