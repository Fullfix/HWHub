from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views import View
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .mixins import ValidDataMixin, check_existance, book_names
from .models import Homework, Grade, Subject, Book
from .utils import load_json, SubjectRus, BookToUrl
from users.models import UserProfile
import json

# Create your views here.

def redirect_hw(request, number, path):
	_1, _2, grade, subject, book, *_ = path.split('/')
	return redirect('bookpage', grade, subject, book, number, 'pop')

def redirect_sort(request, sort, path):
	P = path.split('/')
	if len(P) >= 7:
		_1, _2, grade, subject, book, num, *_ = P
		return redirect('bookpage', grade, subject, book, num, sort)
	else:
		_1, _2, grade, subject, book, *_ = P
		return redirect('grandbookpage', grade, subject, book, sort)

def auto_sort(request, grade, subject, book, num):
	return redirect('bookpage', grade, subject, book, num, 'pop')

def auto_sort_grand(request, grade, subject, book):
	return redirect('grandbookpage', grade, subject, book, 'pop')
	

class ClassPage(View):
	def get(self, request, grade):
		grade_class = Grade.objects.all().get(grade__exact=grade)
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {'user':request.user,
		'profile':profile, 'grade':grade_class}
		return render(request, 'classpage.html', context)

class GrandBookPage(View):
	def get(self, request, grade, subject, book, sort):
		try:
			book = Book.objects.all().get(slug__exact=book)
		except BaseException as e:
			raise Http404(e)
		homeworks = book.homeworks.all()
		if sort == 'pop':
			homeworks = homeworks.likes()
		elif sort == 'new':
			homeworks = homeworks.date()
		else:
			raise Http404(f'фильтра {{sort}} не существует')
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {
			'homeworks':homeworks,
			'book':book, 
			'user':request.user, 
			'profile':profile,
			'sort':sort}
		return render(request, 'bookpage.html', context)


class BookPage(View):
	def get(self, request, grade, subject, book, num, sort='popular'):
		try:
			book = Book.objects.all().get(slug__exact=book)
		except BaseException as e:
			raise Http404(e)		
		homeworks = book.homeworks.all().number(num)
		if sort == 'pop':
			homeworks = homeworks.likes()
		elif sort == 'new':
			homeworks = homeworks.date()
		else:
			raise Http404(f'фильтра {sort} не существует')
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {
			'homeworks':homeworks,
			'book':book, 
			'user':request.user, 
			'profile':profile,
			'cur_num':num,
			'sort':sort}
		return render(request, 'bookpage.html', context)

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
		grades = Grade.objects.all()
		context = {'user':request.user, 
			'profile':profile,
			'grades':grades,
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

