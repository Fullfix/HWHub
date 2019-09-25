from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.http import Http404, HttpResponse
from .models import Homework
from .forms import HomeworkUploadForm
import json

# Create your views here.

def check_if_number_exists(path, p, num):
	with open(path, 'r') as f:
		numbers = json.load(f)
	return str(p) in numbers.keys() and int(numbers[str(p)]) >= num

def books(request):
	return render(request, 'books.html')

def get_hw(request, p, num):
	path = finders.find('maths/alg1.json')
	if not check_if_number_exists(path, p, num):
		return HttpResponse('Number does not exist')
	homeworks = Homework.objects.filter(paragraph__exact = int(p), number__exact = int(num))
	context = {'homeworks': list(homeworks)}
	return render(request, 'maths/hw.html', context)

def upload_hw(request):
	if not request.user.is_authenticated:
		return redirect('login')


	if request.method == 'POST':
		form = HomeworkUploadForm(request.POST, request.FILES)
		if form.is_valid():
			params = form.cleaned_data
			path = finders.find('maths/alg1.json')
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