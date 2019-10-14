from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.staticfiles import finders
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic.base import RedirectView
from .models import Homework
from .forms import HomeworkUploadForm
import json

# Create your views here.

book_names = {'algebra2': 'algebra10profile2'}
book_names_reversed = {'algebra10profile2': 'algebra2'}

def check_if_number_exists(path, p, num):
	with open(path, 'r') as f:
		numbers = json.load(f)
	return str(p) in numbers.keys() and int(numbers[str(p)]) >= num

def books(request):
	return render(request, 'books.html')

def get_hw(request, book, p, num):
	if not book in book_names.keys():
		return HttpResponse('Book does not exist')
	path = finders.find(f'maths/{book_names[book]}.json')
	if not check_if_number_exists(path, p, num):
		return HttpResponse('Number does not exist')


	homeworks = Homework.objects.filter(
		book__exact = book_names[book], 
		paragraph__exact = int(p),
		number__exact = int(num))
	context = {'homeworks': list(homeworks)}
	return render(request, 'maths/hw.html', context)

def upload_hw(request):
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = HomeworkUploadForm(request.POST, request.FILES)
		if form.is_valid():
			params = form.cleaned_data
			path = finders.find('maths/algebra10profile2.json')
			if not check_if_number_exists(path, params['paragraph'], params['number']):
				context = {'form':form, 'number_error':True}
				return render(request, 'maths/upload.html', context)
			homework = Homework.objects.create_homework(params, request.user)
			homework.save()
			return redirect('books')
	else:
		form = HomeworkUploadForm()
	context = {'form':form, 'number_error':False}
	return render(request, 'maths/upload.html', context)


def like_hw(request, id_):
	post = get_object_or_404(Homework, id=id_)
	if request.user in post.likes.all():
		post.likes.remove(request.user)
	elif request.user in post.dislikes.all():
		post.dislikes.remove(request.user)
		post.likes.add(request.user)
	else:
		post.likes.add(request.user)
	return redirect('algebra', 
		book=book_names_reversed[post.book], 
		p=post.paragraph,
		num=post.number)

def dislike_hw(request, id_):
	post = get_object_or_404(Homework, id=id_)
	if request.user in post.dislikes.all():
		post.dislikes.remove(request.user)
	elif request.user in post.likes.all():
		post.likes.remove(request.user)
		post.dislikes.add(request.user)
	else:
		post.dislikes.add(request.user)
	return redirect('algebra', 
		book=book_names_reversed[post.book], 
		p=post.paragraph,
		num=post.number)