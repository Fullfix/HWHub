from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views import View
from users.models import User, UserProfile
from homeworks.models import New
from django.core.mail import send_mail
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from users.forms import UserRegisterForm


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
	login_form = AuthenticationForm
	register_form = UserRegisterForm

	def get(self, request):
		users_num = User.objects.all().count()
		context = {'users':users_num, 'login_form':self.login_form(),
		 'register_form':self.register_form()}
		if request.user.is_authenticated:
			context['is_logged'] = "true"
		else:
			context['is_logged'] = ""
		return render(request, 'landing.html', context)


class LoginUser(View):
    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username and password:
            # Test username/password combination
            user = authenticate(username=username, password=password)
            # Found a match
            if user is not None:
                # User is active
                if user.is_active:
                    # Officially log the user in
                    login(self.request, user)
                    data = {'success': True}
                else:
                    data = {'success': False, 'error': 'User is not active'}
            else:
                if User.objects.filter(username=username).exists():
                    error = _("You entered incorrect password")
                else:
                	error = _("You entered unexisting username")
                data = {'success': False, 'error': error}

            return JsonResponse(data)
        return HttpResponseBadRequest()    


def handler404(request, *args, **kwargs):
	return render(request, '404page.html')

def handler403(request, *args, **kwargs):
	return render(request, '403page.html')

def handler500(request, *args, **kwargs):
	return render(request, '500page.html')