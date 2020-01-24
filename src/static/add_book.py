import json

def add_book(grade, subject, bookname, url, name):
	with open(f"algebra/{bookname}", 'r', encoding='utf8') as f:
		book_dict = json.load(f)
	with open('homeworks.json', 'r', encoding='utf8') as f:
		json_dict = json.load(f)
	print(json_dict)
	json_dict[str(grade)][subject].append([url, name, book_dict])
	with open('homeworks.json', 'w', encoding='utf8') as f:
		json.dump(json_dict, f, ensure_ascii=False)

if __name__ == "__main__":
	add_book(10, "algebra", "algebra10profile2.json",
	 "algebra10profile2", "Алгебра 10 класс профиль 2 часть")