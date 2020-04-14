from homeworks.models import Book, Subject
import json

with open("numbers_algebra.json", 'rb') as f:
	A = json.load(f)

B = Book.objects.all().filter(name="algebra10profile2")[0]
T = [["", "Упражения"]]
B.set_types(T)
B.save()