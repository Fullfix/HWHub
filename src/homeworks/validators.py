from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(image):
	width, height = get_image_dimensions(image)
	if height / width > 20/9:
		raise ValidationError(
			f"Высота файла {height} слишком большая по сравнению с шириной {width}")