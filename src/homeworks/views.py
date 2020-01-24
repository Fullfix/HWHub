from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views import View
from .mixins import ValidDataMixin, check_existance
from .models import Homework
from users.models import UserProfile
import json

# Create your views here.

def get_json_file(request):
	with open (finders.find('homeworks.json'), 'r', encoding='utf8') as f:
		json_file = json.load(f)
	return JsonResponse(json_file)

class ClassPage(View):
	def get(self, grade):
		pass

class BookPage(View):
	def get(self, grade, subject, book):
		pass

class GetHW(ValidDataMixin, View):
	def get(self, request, grade, subject, book, p, num):
		homeworks = Homework.objects.all().number(grade, subject, book, p, num)
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {'homeworks': list(homeworks), 'user': request.user, 'profile':profile}
		return render(request, 'hw.html', context)


@method_decorator(login_required, name='dispatch')
class GetHWOpinion(View):
	def get(self, request):
		post = get_object_or_404(Homework, id=request.GET['homework_id'])
		if request.user in post.likes.all():
			liked = True
		else:
			liked = False
		if request.user in post.dislikes.all():
			disliked = True
		else:
			disliked = False
		json = {"liked":liked, "disliked":disliked}
		return JsonResponse(json)


@method_decorator(login_required, name='dispatch')
class UploadHW(View):
	template_name = 'upload.html'
	def get(self, request):
		profile = UserProfile.objects.filter(user=request.user)[0]
		context = {'user':request.user, 
			'profile':profile,
			'number_error':False,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		context = {'error': False, 'created': False }
		params = dict(request.POST)
		files = dict(request.FILES)
		for key, value in params.items():
			params[key] = value[0]
		for key, value in files.items():
			files[key] = value[0]
		p, num = params['number'].split('.')
		params['paragraph'] = int(p)
		params['number'] = int(num)
		homework = Homework.objects.create_homework(params, files, request.user)
		context['created'] = True
		return JsonResponse(context)


@method_decorator(login_required, name='dispatch')
class LikeHW(View):
	def get(self, request):
		post = get_object_or_404(Homework, id=request.GET['homework_id'])
		if request.user in post.likes.all():
			post.likes.remove(request.user)
			liked = False
			undisliked = False
		elif request.user in post.dislikes.all():
			post.dislikes.remove(request.user)
			post.likes.add(request.user)
			liked = True
			undisliked = True
		else:
			post.likes.add(request.user)
			liked = True
			undisliked = False
		json = {'likes':post.likes.count(), 'dislikes':post.dislikes.count(),
		'liked':liked, 'undisliked':undisliked}
		return JsonResponse(json)


@method_decorator(login_required, name='dispatch')
class DislikeHW(View):
	def get(self, request):
		post = get_object_or_404(Homework, id=request.GET['homework_id'])
		if request.user in post.dislikes.all():
			post.dislikes.remove(request.user)
			disliked = False
			unliked = False
		elif request.user in post.likes.all():
			post.likes.remove(request.user)
			post.dislikes.add(request.user)
			disliked = True
			unliked = True
		else:
			post.dislikes.add(request.user)
			disliked = True
			unliked = False
		json = {'likes':post.likes.count(), 'dislikes':post.dislikes.count(),
		'disliked':disliked, 'unliked':unliked}
		return JsonResponse(json)

