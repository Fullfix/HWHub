from homeworks.models import Book, Subject
import json

def get_number_list():
	with open("numbers_algebra.json", 'rb') as f:
		A = json.load(f)
	B = []
	for i in range(1, int(A['numbers'])+1):
		B.append(str(i))
	for i in A['after']:
		for j in range(1, int(A['after'][i])+1):
			B.append(i+'a'+str(j))
	for i in range(1, int(A['repeatition'])+1):
		B.append('p'+str(i))
	for i in range(1, int(A['hard'])+1):
		B.append('h'+str(i))
	return B

A = get_number_list()
Algebra = Subject.objects.all().filter(name="algebra")[0]
P = {
	"name": "algebra1011",
	"full_name":"Алгебра 10-11",
	"slug": "algebra1011",
	"subject": Algebra,
}
B = Book(**P)
B.set_numbers(A)
B.save()