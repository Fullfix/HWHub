from django.contrib.staticfiles import finders
from django.http import Http404
import json

book_names = {
	'algebra2': 'algebra10profile2'
}

def check_existance(grade, subject, book, p, num, url=True):
	with open(finders.find('homeworks.json'), 'r', encoding='utf8') as f:
		json_file = json.load(f)
	if not str(grade) in json_file.keys():
		return 'grade'
	if not subject in json_file[str(grade)].keys():
		return 'subject'

	if not book_names[book] in [i[0] for i in json_file[str(grade)][subject]]:
		return 'book'
	else:
		for i in json_file[str(grade)][subject]:
			if book_names[book] == i[0]:
				book_json = i[2]
				break
	if not str(p) in book_json.keys():
		return 'paragraph'
	if not int(num) in range(1, int(book_json[str(p)])+1):
		return 'number'
	return False


class ValidDataMixin(object):
	def dispatch(self, request, grade, subject, book, par, num, sort):
		error = check_existance(grade, subject, book, par, num)
		if error == 'grade':
			raise Http404(f'Класса "{grade}" не существует')
		if error == 'subject':
			raise Http404(f'Предмета "{subject}" не существует')
		elif error == 'book':
			raise Http404(f'Книги "{book_names[book]}" в предмете "{subject}" не существует')
		elif error == 'paragraph':
			raise Http404(
				f'Параграфа {par} в книге "{book}" в предмете "{subject}" не существует')
		elif error == 'number':
			raise Http404(
				f'Номера {num} в параграфе {par} ' +
				'в книге "{book}" в предмете "{subject}" не существует')
		return super(ValidDataMixin,self).dispatch(request, grade, subject, book, par, num, sort)