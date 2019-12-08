from django import forms
from .models import Homework

class HomeworkUploadForm(forms.ModelForm):
	class Meta:
		model = Homework
		fields = ['subject', 'book', 'paragraph', 'number', 'image']