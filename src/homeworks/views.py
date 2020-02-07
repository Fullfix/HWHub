from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views import View
from django.core import serializers
from .mixins import ValidDataMixin, check_existance, book_names
from .models import Homework
from .utils import load_json
from users.models import UserProfile
import json

# Create your views here.

def get_json_file(request):
	json_file = load_json()
	return JsonResponse(json_file)

def redirect_hw(request, number, path):
	_1, _2, grade, subject, book, *_ = path.split('/')
	p, num = number.split('.')
	return redirect('bookpage', grade, subject, book, p, num)

def redirect_sort(request, sort, path):
	P = path.split('/')
	if len(P) >= 7:
		_1, _2, grade, subject, book, par, num, *_ = P
		return redirect('bookpage', grade, subject, book, par, num, sort)
	else:
		_1, _2, grade, subject, book, *_ = P
		return redirect('grandbookpage', grade, subject, book, sort)

def auto_sort(request, grade, subject, book, par, num):
	return redirect('bookpage', grade, subject, book, par, num, 'pop')

def auto_sort_grand(request, grade, subject, book):
	return redirect('grandbookpage', grade, subject, book, 'pop')

class ClassPage(View):
	def get(self, request, grade):
		grade = str(grade)
		with open(finders.find('homeworks.json'), 'r', encoding='utf8') as f:
			json_file = json.load(f)
		SubjectList = []
		for subject, Books in json_file[grade].items():
			SubjectList.append([subject, [book[0] for book in Books]])
		print(SubjectList)
		if request.user.is_authenticated:
			profile = UserProfile.objects.filter(user=request.user)[0]
		else:
			profile = None
		context = {'subjects': SubjectList, 'user':request.user, 'profile':profile, 'class':grade}
		return render(request, 'classpage.html', context)

class GrandBookPage(View):
	def get(self, request, grade, subject, book, sort):
		json_file = load_json()
		try:
			for i in json_file[str(grade)][subject]:
				if i[0] == book_names[book]:
					book_file = i[2]
					title = i[1]
					break
		except BaseException as e:
			raise Http404(e)

		BookList = []
		for p, maxn in book_file.items():
			for n in range(1, int(maxn)+1):
				BookList.append(f'{p}.{n}')
		homeworks = Homework.objects.all().book(grade, subject, book_names[book])
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
		context = {'title': title,
			'image': f'images/{book_names[book]}.jpg',
			'homeworks':homeworks,
			'book':BookList, 
			'user':request.user, 
			'profile':profile,
			'sort':sort}
		return render(request, 'bookpage.html', context)


class BookPage(ValidDataMixin, View):
	def get(self, request, grade, subject, book, par, num, sort='popular'):
		json_file = load_json()
		for i in json_file[str(grade)][subject]:
			if i[0] == book_names[book]:
				book_file = i[2]
				title = i[1]
				break
		BookList = []
		for p, maxn in book_file.items():
			for n in range(1, int(maxn)+1):
				BookList.append(f'{p}.{n}')
		homeworks = Homework.objects.all().number(grade, subject, book_names[book], par, num)
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
		context = {'title': title,
			'image': f'images/{book_names[book]}.jpg',
			'homeworks':homeworks,
			'book':BookList, 
			'user':request.user, 
			'profile':profile,
			'cur_num':f'{par}.{num}',
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

