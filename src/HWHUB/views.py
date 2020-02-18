from django.shortcuts import render
from django.views import View
from users.models import User, UserProfile
from homeworks.models import New

class MainPage(View):
	def get(self, request):
		last_users = User.objects.all().last()[:10]
		last_news = New.objects.all().order_by('-publication_date')
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {'user':request.user, 'profile':profile,
		'last_users':last_users, 'last_news':last_news}
		return render(request, 'main.html', context)