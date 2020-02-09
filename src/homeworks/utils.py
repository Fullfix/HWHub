import datetime
import pytz
import json
from django.conf import settings
from django.contrib.staticfiles import finders

SubjectRus = {
	'algebra': 'Алгебра',
	'geomety': 'Геометрия',
	'physics': 'Физика',
}

BookToUrl = {
	'algebra10profile2': 'algebra2'
}

def create_grades():
	C = []
	for i in range(1, 12):
		C.append((i, str(i)))
	return tuple(C)

def time_to_string(date):
	timezone = pytz.timezone(settings.TIME_ZONE)
	upload = date.astimezone(timezone)
	now = timezone.localize(datetime.datetime.now())
	d = now - upload
	year = datetime.timedelta(days=365)
	month = datetime.timedelta(days=30)
	week = datetime.timedelta(days=7)
	day = datetime.timedelta(days=1)
	hour = datetime.timedelta(hours=1)
	minute = datetime.timedelta(minutes=1)
	second = datetime.timedelta(seconds=1)
	s = ''
	if d // year:
		s = f'{d // year} год назад'
	elif d // month:
		s = f'{d // month} месяцев назад'
	elif d // week:
		s = f'{d // week} недель назад'
	elif d // day:
		s = f'{d // day} дней назад'
	elif d // hour:
		s = f'{d // hour} часов назад'
	elif d // minute:
		s = f'{d // minute} минут назад'
	elif d // second:
		s = f'{d // second} секунд назад'
	return s

def upload_location(instance, filename):
	return 'uploads/%s/%s.%s' % (instance.homework.publisher.id,
		instance.homework.id,
		filename.split('.')[-1])

def load_json():
	with open(finders.find('homeworks.json'), 'r', encoding='utf8') as f:
		json_file = json.load(f)
	return json_file