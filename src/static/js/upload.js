function get_object(url) {
    var instance = [];
    $.ajax({
        url: url,
        async: false,
        success: (json) => {instance = json}
    })
    return instance
}

function get_choices(list) {
    return list.map(url => {
        let obj = get_object(url);
        return {"value":obj.url, "fullname":obj.full_name}
    })
}

function create_hw(form, uploadedFiles) {
    formdata = new FormData(form);
    data = new FormData(document.getElementById("upload_form"));
    formdata.forEach((value, key) => {
        if (key == "grade") {
            data.append(key, get_object(value).id);
        }
        else if (key == "subject" || key == "book") {
            data.append(key, get_object(value).id);
        }
        else {
            data.append(key, value)
        }
    })
    uploadedFiles.forEach((value, key) => data.append('file'+key, value))
    fetch('/api/create_homework', { // Your POST endpoint
    method: 'POST',
    body: data // This is your file object
    }).then(
        response => response.json() // if the response is a JSON object
    ).then(response => {
        console.log(response)
        if (response.success) {
            let url = window.location.href.replace(/#upload_frame/g, '');
            window.location.href = url;
        }
        else {
            alert("Выберите все поля и добавьте файл вашего домашнего задания");
        }
    })
}

function getNumberType(number, numberDict, types) {
    for (let k in numberDict) {
        for (let i in numberDict[k]) {
            if (k + numberDict[k][i] == number) {
                for (let j in types) {
                    if (types[j][0] == k) {
                        name = types[j][1];
                    }
                }
                return [name, numberDict[k][i]];
            }
        }
    }
}

function uploadMain() {
    var grades = get_object('/api/grades/')
    var grade = $('#div_input_grade');
    var grade_select = grade.find('.input_hw');
    var subject = $('#div_input_subject');
    var subject_select = subject.find('.input_hw');
    var book = $('#div_input_book');
    var book_select = book.find('.input_hw');
    var number = $('#div_input_number');
    var number_select = number.find('.input_hw');
    var file = $('#file_input');
    var btn = $('#upload_btn');
    var dropzone = $('#dropzone');
    var uploadedFiles = [];
    var grade = 10
    var currentChoices = ["10"]
    var jsonBooks = null;
    var jsonNumbers = null;

    document.getElementById("filechoose").onchange = function(e) {
        Array.from(this.files).forEach(function(file){
            if (!['png', 'jpg', 'jpeg'].includes(file.name.split('.').pop())) {
                alert("Файл должен быть с расширением .png/.jpg/.jpeg");
            }
            else {
                if (uploadedFiles.length == 0) {
                    btn.removeClass('invis');
                }
                uploadedFiles.push(file);
                $('#uploads').append('<h5 class="names">'+file.name+'</h5>');
                $('#uploads h5:last').on("click", function() {
                    for (let i = 0; i < uploadedFiles.length; i++) {
                        if (uploadedFiles[i].name == $(this).text()) {
                            uploadedFiles.splice(i, 1);
                            break;
                        }
                    }
                    $(this).remove();
                    if (uploadedFiles.length == 0) {
                        btn.addClass('invis');
                    }
                })
            }
        })
    }

    $('#post-form').on('submit', function(e) {
        console.log("submit")
        e.preventDefault()
        grade_select.attr("disabled", false)
        subject_select.attr("disabled", false);
        book_select.attr("disabled", false);
        number_select.attr("disabled", false);
        create_hw(this, uploadedFiles);
    })


    dropzone.on("dragover", function() {
        $(this).addClass('dragover');
        return false;
    })

    dropzone.on("dragleave", function() {
        $(this).removeClass('dragover');
    })

    dropzone.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass('dragover');
        e.dataTransfer = e.originalEvent.dataTransfer;
        Array.from(e.dataTransfer.files).forEach(function(file){
            if (!['png', 'jpg', 'jpeg'].includes(file.name.split('.').pop())) {
                alert("Файл должен быть с расширением .png/.jpg/.jpeg");
            }
            else {
                if (uploadedFiles.length == 0) {
                    btn.removeClass('invis');
                }
                uploadedFiles.push(file);
                $('#uploads').append('<h5 class="names">'+file.name+'</h5>');
                $('#uploads h5:last').on("click", function() {
                    for (let i = 0; i < uploadedFiles.length; i++) {
                        if (uploadedFiles[i].name == $(this).text()) {
                            uploadedFiles.splice(i, 1);
                            break;
                        }
                    }
                    $(this).remove();
                    if (uploadedFiles.length == 0) {
                        btn.addClass('invis');
                    }
                })
            }
        })
    })

    $('#go_back_img').on('click', function() {
        if (grade_select.attr("disabled") && !subject_select.attr("disabled")) {
            grade_select.attr("disabled", false);
            grade_select.attr("value", 'not chosen');
            subject.addClass("invis");
            subject_select.empty()
            subject_select.append(
            '<option hidden disabled selected value="not chosen">-- Выберите предмет --</option>'
            )
        }
        if (subject_select.attr("disabled") && !book_select.attr("disabled")){
            subject_select.attr("disabled", false);
            subject_select.attr("value", 'not chosen');
            book.addClass("invis");
            book_select.empty()
            book_select.append(
            '<option hidden disabled selected value="not chosen">-- Выберите книгу --</option>'
            )
        }
        else if (book_select.attr("disabled") && !number_select.attr("disabled")){
            book_select.attr("disabled", false);
            book_select.attr("value", 'not chosen');
            number.addClass("invis");
            number_select.empty()
            number_select.append(
            '<option hidden disabled selected value="not chosen">-- Выберите параграф --</option>'
            )
        }
        else if (number_select.attr("disabled")) {
            number_select.attr("disabled", false);
            number_select.attr("value", 'not chosen');
            file.addClass("invis");
            if (!btn.hasClass("invis")) {
                btn.addClass("invis");
            }
            uploadedFiles = [];
            $('#uploads').empty();
        }
    })

    grade_select.on('change', function() {
        currentChoices = get_choices(get_object(this.value).subjects);
        currentChoices.forEach((subject => {
            subject_select.append('<option value="'+subject.value+'">'+subject.fullname+'</option')
        }));
        subject.removeClass("invis");
        grade_select.attr("disabled", true);
    })

    subject_select.on('change', function() {
        currentChoices = get_choices(get_object(this.value).books);
        currentChoices.forEach(function(book) {
            book_select.append('<option value="'+book.value+'">'+book.fullname+'</option>');
        })
        book.removeClass("invis");
        subject_select.attr("disabled", true);
    })

    book_select.on('change', async function() {
        let numberDict;
        let Arr;
        let name;
        let num;
        let obj = get_object(this.value);
        let types = JSON.parse(obj.type_list);
        currentChoices = JSON.parse(obj.number_list);
        await fetch('/api/get_book_number_dict/' + obj.id, {
            method: "GET",
        }).then(response => response.json())
        .then(response => numberDict = response);
        currentChoices.forEach(number => {
            Arr = getNumberType(number, numberDict, types);
            name = Arr[0];
            num = Arr[1];
            number_select.append('<option value="'+number+'">'+ name + " "+ num + '</option');
        })
        number.removeClass("invis");
        book_select.attr("disabled", true);
    })

    number_select.on('change', function() {
        file.removeClass("invis");
        number_select.attr("disabled", true);
    })
}