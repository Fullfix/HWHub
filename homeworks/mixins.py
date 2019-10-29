from django.contrib.staticfiles import finders
from django.http import Http404
import json

book_names = {'algebra2': 'algebra10profile2'}

def check_existance(subject, book, p, num, url=True):
	with open (finders.find('books.json'), 'r', encoding='utf8') as f:
		books_file = json.load(f)
	if not subject in books_file.keys():
		return 'subject'
	if url and book not in book_names.keys():
		return 'book'
	else: book = book_names[book]
	if not any(book == b[0] for b in books_file[subject]):
		return 'book'
	with open(finders.find(f'{subject}/{book}.json'), 'r', encoding='utf8') as f:
		numbers_file = json.load(f)
	if not str(p) in numbers_file.keys():
		return 'paragraph'
	if int(num) not in range(1, int(numbers_file[str(p)])+1):
		return 'number'
	return False


class ValidDataMixin(object):
	def dispatch(self, request, subject, book, p, num):
		error = check_existance(subject, book, p, num)
		if error == 'subject':
			raise Http404(f'Предмета "{subject}" не существует')
		elif book not in book_names.keys() or error == 'book':
			raise Http404(f'Книги "{book}" в предмете "{subject}" не существует')
		elif error == 'paragraph':
			raise Http404(
				f'Параграфа {p} в книге "{book}" в предмете "{subject}" не существует')
		elif error == 'number':
			raise Http404(
				f'Номера {num} в параграфе {p} ' +
				'в книге "{book}" в предмете "{subject}" не существует')
		return super(ValidDataMixin, self).dispatch(request, subject, book_names[book], p, num)