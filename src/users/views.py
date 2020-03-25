from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import UserRegisterForm
from .models import UserProfile, User
from homeworks.models import Homework


class RegisterView(View):
	form_class = UserRegisterForm
	template_name = 'registration/register.html'

	def get(self, request):
		form = self.form_class()
		context = {'form': form}
		return render(request, self.template_name, context)

	def post(self, request):
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
			return redirect('main')
		else:
			context = {'form': form}
			return render(request, self.template_name, context)


@login_required
def profile(request, id_):
	user = get_object_or_404(User, id=id_)
	profile = user.profile
	homeworks = Homework.objects.all().publisher(user)
	context = {'user':request.user, 'page_user':user, 'profile':profile, 'homeworks':homeworks}
	return render(request, 'users/profile.html', context)