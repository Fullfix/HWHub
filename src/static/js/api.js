function getObject(url) {
    var instance = [];
    $.ajax({
        url: url,
        async: false,
        success: (json) => {instance = json}
    })
    return instance
}

function loadBooks() {
	var books = getObject('/api/books');
	books = books.map(book => {
		subjectJSON = getObject(book.subject);
		subject = subjectJSON.full_name;
		gradeJSON = getObject(subjectJSON.grade);
		grade = gradeJSON.grade
		return [grade + '/' + subject + '/', book.full_name]
	})
	return books;
}

function loadSubjects() {
	var subjects = getObject('/api/subjects');
	subjects = subjects.map(subject => {
		gradeJSON = getObject(subject.grade);
		grade = gradeJSON.grade
		return [grade + '/', subject.full_name]
	})
	return subjects;
}

function inputToUrl(input) {
	var url, grade, subject, subject_inp, L;
	if (input.includes('/')) {
		L = input.split('/');
		grade = L[0];
		subject_inp = L[1];
		getObject('/api/subjects').forEach(subject => {
			if (subject.full_name == subject_inp) {
				url = '/' + grade;
			}
		})
	}
	else {
		getObject('/api/books').forEach(book => {
			if (book.full_name == input) {
				subject = getObject(book.subject);
				grade = getObject(subject.grade).grade;
				url = '/' + grade + '/' + subject.name + '/' + book.slug;
			}
		})
	}
	return '/homework' + url;
}