from django import forms
from .models import User, UserProfile
# from .validators import validate_username
from django.contrib.auth.forms import UserCreationForm

def create_grades():
	C = []
	for i in range(1, 12):
		C.append((i, str(i)))
	return tuple(C)


# class UserNameField(forms.CharField):
# 	default_validators = [validate_username]


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(max_length=20, label='Ник')
	name = forms.CharField(max_length=15, label='Имя', required=False)
	surname = forms.CharField(max_length=15, label='Фамилия', required=False)
	grade = forms.ChoiceField(choices=create_grades(), label='Класс', required=False)
	password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
	password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

	username.widget.attrs.update({'class':'register_input', 'id':'username'})
	name.widget.attrs.update({'class':'register_input', 'id':'name'})
	surname.widget.attrs.update({'class':'register_input', 'id':'surname'})
	grade.widget.attrs.update({'class':'register_input', 'id':'grade'})
	password1.widget.attrs.update({'class':'register_input', 'id':'password1'})
	password2.widget.attrs.update({'class':'register_input', 'id':'password2'})

	class Meta:
		model = User
		fields = ('username', 'name', 'surname', 'grade')


	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2