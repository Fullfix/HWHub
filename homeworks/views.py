from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from django.views import View
from .models import Homework
from users.models import UserProfile
import json

# Create your views here.

book_names = {'algebra2': 'algebra10profile2'}

def check_if_number_exists(path, p, num):
	with open(path, 'r') as f:
		numbers = json.load(f)
	return str(p) in numbers.keys() and int(numbers[str(p)]) >= num

def books(request):
	return render(request, 'books.html')

def get_json_books(request):
	with open (finders.find('books.json'), 'r', encoding='utf8') as f:
		json_file = json.load(f)
	return JsonResponse(json_file)

def get_json_numbers(request):
	book = request.GET['book']
	with open (finders.find(f'algebra/{book}.json'), 'r', encoding='utf8') as f:
		json_file = json.load(f)
	return JsonResponse(json_file)

def check_existance(subject, book, p, num, url=True):
	with open (finders.find('books.json'), 'r', encoding='utf8') as f:
		books_file = json.load(f)
	if not subject in books_file.keys():
		return 'subject'
	if url and book not in book_names.keys():
		return 'book'
	else: book = book_names[book]
	if not any(book == b[0] for b in books_file[subject]):
		return 'book'
	with open(finders.find(f'{subject}/{book}.json'), 'r', encoding='utf8') as f:
		numbers_file = json.load(f)
	if not str(p) in numbers_file.keys():
		return 'paragraph'
	if int(num) not in range(1, int(numbers_file[str(p)])+1):
		return 'number'
	return None

def get_hw(request, subject, book, p, num):
	error = check_existance(subject, book, p, num)
	if error == 'subject':
		return HttpResponse(f'Предмета "{subject}" не существует')
	elif book not in book_names.keys() or error == 'book':
		return HttpResponse(f'Книги "{book}" в предмете "{subject}" не существует')
	elif error == 'paragraph':
		return HttpResponse(
			f'Параграфа {p} в книге "{book}" в предмете "{subject}" не существует')
	elif error == 'number':
		return HttpResponse(
			f'Номера {num} в параграфе {p} ' +
			'в книге "{book}" в предмете "{subject}" не существует')

	homeworks = Homework.objects.filter(
		book__exact = book_names[book], 
		paragraph__exact = int(p),
		number__exact = int(num))
	profile = UserProfile.objects.filter(user=request.user)[0]
	context = {'homeworks': list(homeworks), 'user': request.user, 'profile':profile}
	return render(request, 'hw.html', context)


@method_decorator(login_required, name='get')
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


@method_decorator(login_required, name='get')
class UploadHW(View):
	template_name = 'upload.html'
	def get(self, request):
		profile = UserProfile.objects.filter(user=request.user)[0]
		context = {'user':request.user, 'profile':profile, 'number_error':False}
		return render(request, self.template_name, context)

	def post(self, request):
		context = {'error': False, 'created': False }
		params = dict(request.POST)
		files = dict(request.FILES)
		for key, value in params.items():
			params[key] = value[0]
		for key, value in files.items():
			files[key] = value[0]
		# if finders.find(f'{params['subject']}') == []:
		# 	context['error'] = f'Предмета {params['subject']} не существует'
		# 	return JsonResponse(context)
		# path = finders.find(f'{params['subject']/{params['book']}}')
		# if path == []:
		# 	context['error'] = f'Книги {params['book']} не существует'
		# 	return JsonResponse(context)
		# with open(context, 'r') as f:
		# 	D = json.load(f)
		# if not params['paragraph'] in D.keys():
		# 	context['error'] = f'Параграфа {params['paragraph']} не существует'
		# 	return JsonResponse(context)
		# if not params['number'] in D[params['paragraph']]:
		# 	context['error'] = f'Номера {params['number']} не существует'
		# 	return JsonResponse(context)

		homework = Homework.objects.create_homework(params, files, request.user)
		context['created'] = True
		return JsonResponse(context)


@method_decorator(login_required, name='get')
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


@method_decorator(login_required, name='get')
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

