from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_image(image):
	width, height = get_image_dimensions(image)
	if height / width > 20/9:
		raise ValidationError(
			f"Высота файла {height} слишком большая по сравнению с шириной {width}")

def validate_json_file(file):
	ext = file.name.split('.')[-1]
	if ext != 'json':
		raise ValidationError(f"file {file.name} has extention .{ext} instead of '.json'")