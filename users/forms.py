from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def create_grades():
	C = []
	for i in range(1, 12):
		C.append((i, str(i)))
	return tuple(C)


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=20, label='Ник')
	name = forms.CharField(max_length=15, label='Имя')
	surname = forms.CharField(max_length=15, label='Фамилия')
	grade = forms.ChoiceField(choices=create_grades(), label='Класс')
	password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
	password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']

	username.widget.attrs.update({'class':'register_input', 'id':'username'})
	name.widget.attrs.update({'class':'register_input', 'id':'name'})
	surname.widget.attrs.update({'class':'register_input', 'id':'surname'})
	grade.widget.attrs.update({'class':'register_input', 'id':'grade'})
	password1.widget.attrs.update({'class':'register_input', 'id':'password1'})
	password2.widget.attrs.update({'class':'register_input', 'id':'password2'})