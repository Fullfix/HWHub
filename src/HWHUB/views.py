from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from users.models import User, UserProfile
from homeworks.models import New
from django.core.mail import send_mail
from django.template import RequestContext


@method_decorator(login_required, name='dispatch')
class MainPage(View):
	def get(self, request):
		last_users = User.objects.all().last()[:10]
		last_news = New.objects.all().order_by('-publication_date')
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {'user':request.user, 'profile':profile,
		'last_users':last_users, 'last_news':last_news, 'classes':list(range(1, 12))}
		return render(request, 'main.html', context)


class LandingPage(View):
	def get(self, request):
		users_num = User.objects.all().count()
		context = {'users':users_num}
		return render(request, 'landing.html', context)


def handler404(request, *args, **kwargs):
	return render(request, '404page.html')

def handler403(request, *args, **kwargs):
	return render(request, '403page.html')

def handler500(request, *args, **kwargs):
	return render(request, '500page.html')