function autocomplete(inp) {
	const books = loadBooks();
	const subjects = loadSubjects();
	var submitBtn = document.getElementById("submit_btn");
	var inp = document.getElementById("search");
	var currentFocus;
	inp.addEventListener("input", (e) => {
		var a, b, i;
		var val = inp.value;
		closeAllLists();
		if (!val) { return false; }
		currentFocus = -1;
		a = document.createElement("DIV");
		a.setAttribute("id", "autocomplete-list");
		a.setAttribute("class", "autocomplete-items usual");
		inp.parentNode.appendChild(a);
		for (i=0; i<books.length; i++) {
			if (books[i][1].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				b = document.createElement("DIV");
				b.innerHTML = books[i][0];
				b.innerHTML += "<strong>" + books[i][1].substr(0, val.length) + "</strong>";
				b.innerHTML += books[i][1].substr(val.length);
				b.innerHTML += " (учебник)"
				b.innerHTML += "<input type='hidden' value='" + books[i][1] + "'>";
				b.addEventListener("click", function(e) {
					inp.value = this.getElementsByTagName("input")[0].value;
					closeAllLists();
					checkSubmit();
				})
				a.appendChild(b);
			}
		}
		for (i=0; i<subjects.length; i++) {
			if (subjects[i][1].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
				b = document.createElement("DIV");
				b.innerHTML = subjects[i][0];
				b.innerHTML += "<strong>" + subjects[i][1].substr(0, val.length) + "</strong>";
				b.innerHTML += subjects[i][1].substr(val.length);
				b.innerHTML += " (предмет)"
				b.innerHTML += "<input type='hidden' value='" + subjects[i][0] + subjects[i][1] + "'>";
				b.addEventListener("click", function(e) {
					inp.value = this.getElementsByTagName("input")[0].value;
					closeAllLists();
					checkSubmit();
				})
				a.appendChild(b);
			}
		}
		checkSubmit();
	})

	inp.addEventListener("keydown", (e) => {
		var x = document.getElementById("autocomplete-list");
		if (x) x = x.getElementsByTagName("div");
		if (e.keyCode == 40) {
			currentFocus++;
			addActive(x);
		}
		else if (e.keyCode == 38) {
			currentFocus--;
			addActive(x);
		}
		else if (e.keyCode == 13) {
			e.preventDefault();
			if (currentFocus > -1) {
				if (x) x[currentFocus].click();
			}
		}
	})

	function addActive(x) {
		if (!x) return false;
		removeActive(x);
		if (currentFocus >= x.length) currentFocus = 0;
    	if (currentFocus < 0) currentFocus = (x.length - 1);
    	x[currentFocus].classList.add("autocomplete-active");
	}

	function removeActive(x) {
		for (var i = 0; i < x.length; i++) {
      		x[i].classList.remove("autocomplete-active");
    	}
	}

	function closeAllLists(elmnt) {
		 var x = document.getElementsByClassName("autocomplete-items");
		 for (var i = 0; i < x.length; i++) {
		 	if (elmnt != x[i] && elmnt != inp) {
		 		x[i].parentNode.removeChild(x[i]);
		 	}
		 }
    }

    function checkSubmit() {
    	books.forEach(book => {
    		if (book[1] == inp.value) {
    			submitBtn.disabled = false;
    			submitBtn.classList.remove('disabled');
    			return true;
    		}
    	})
    	subjects.forEach(subject => {
    		console.log(subject[0]+subject[1])
    		if (subject[0]+subject[1] == inp.value) {
    			submitBtn.disabled = false;
    			submitBtn.classList.remove('disabled');
    			return true;
    		}
    	})
    	return false;
    }

    document.addEventListener("click", (e) => {
    	closeAllLists(e.target);
    });

    submitBtn.addEventListener("click", function(e) {
    	if (!this.disabled) {
    		var url = inputToUrl(inp.value);
    		if (url) {
    			window.location.href = url;
    		}
    	}
	})
}