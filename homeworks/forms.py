from django import forms
from .models import Homework

class HomeworkUploadForm(forms.Form):
	book = forms.CharField(max_length=30)
	paragraph = forms.IntegerField()
	number = forms.IntegerField()
	image = forms.ImageField()