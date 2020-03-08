function setDropzone() {
    let dropzone = document.getElementById("profile_dropzone");
    let uploadedFiles = [];
    dropzone.on("dragover", function() {
        $(this).addClass('profile_dragover');
        return false;
    })

    dropzone.on("dragleave", function() {
        $(this).removeClass('profile_dragover');
    })

    dropzone.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass('profile_dragover');
        e.dataTransfer = e.originalEvent.dataTransfer;
        Array.from(e.dataTransfer.files).forEach(function(file){
            if (['png', 'jpg', 'jpeg'].contains(file.name.split('.').pop())) {
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
}