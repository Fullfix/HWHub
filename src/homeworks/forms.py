from django import forms
from .models import Homework, Book
from .validators import validate_json_file
import json

class AbstractBookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['name', 'full_name', 'slug', 'subject', 'image']


class BookUploadForm(AbstractBookForm):
	numbers_json = forms.FileField(max_length=10000, validators=[validate_json_file])
	types_json = forms.FileField(max_length=10000, validators=[validate_json_file])

	class Meta(AbstractBookForm.Meta):
		fields = AbstractBookForm.Meta.fields + ['numbers_json', 'types_json']

	def save(self, commit=True):
		data = self.cleaned_data
		types_dict = json.load(data['types_json'])
		numbers_dict = json.load(data['numbers_json'])
		data['numbers_json'] = numbers_dict
		data['types_json'] = types_dict
		book = Book.objects.create_by_number_range(commit=commit, **data)
		self.save_m2m = self._save_m2m
		return book
