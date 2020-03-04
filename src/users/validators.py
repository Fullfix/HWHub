from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_input(value):
	for i in "#!*'();:@&=+$,/?%[]":
	    if i in value:
	        raise ValidationError(
	            _(f'Поле содержит недопустимые символы'),
	            params={'value': value},
	        )