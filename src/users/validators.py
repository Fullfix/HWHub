from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_input(value):
	for i in "#!*'();:@&=+$,/?%[]":
	    if i in value:
	        raise ValidationError(
	            _(f'Field contains inappropriate symbols'),
	            params={'value': value},
	        )