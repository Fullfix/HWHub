from django import forms
from .models import Homework

class HomeworkUploadForm(forms.ModelForm):
	class Meta:
		model = Homework
		fields = ['book', 'paragraph', 'number', 'image']