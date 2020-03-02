HWMain = function() {
    console.log("main")
    var hwButtons = document.getElementsByClassName("Homework_buttons");
    var imageGrids = document.getElementsByClassName('Homework_img');

    for (let btns of hwButtons) {
        let hwid = $(btns).attr("data-hwid");
        let imgLike = $(btns).find('.like_img');
        let imgDislike = $(btns).find('.dislike_img');
        $.ajax({
            type: "GET",
            url: "/homework/get_opinion",
            dataType: "JSON",
            data: {homework_id: hwid},
            success: function(json) {
                if (json.liked) {
                    $(imgLike).attr("src", "../images/like_btn_liked.png")
                }
                else {
                    $(imgLike).attr("src", "../images/like_btn.png")
                }
                if (json.disliked) {
                    $(imgDislike).attr("src", "../images/dislike_btn_disliked.png")
                }
                else {
                    $(imgDislike).attr("src", "../images/dislike_btn.png")
                }
            }
        })
    }
}

function getImagesWidth (images) {
    return images[0].width / images.length;
}

function likeHW (btn) {
    var hwid = $(btn).attr("data-hwid");
    var div = $('#hw_buttons'+hwid);
    $.ajax({
        type: "GET",
        url: "/homework/like/",
        dataType: "JSON",
        data: {homework_id: hwid},
        success: function(json) {
            div.find('.Homework_like_count').html(json.likes);
            div.find('.Homework_dislike_count').html(json.dislikes);
            var imgLike = div.find('.like_img');
            var imgDislike = div.find('.dislike_img');
            if (json.liked) {
                $(imgLike).attr("src", "../images/like_btn_liked.png");
                if (json.undisliked) {
                    $(imgDislike).attr("src", "../images/dislike_btn.png");
                }
            }
            else {
                $(imgLike).attr("src", "../images/like_btn.png");
            }
        }
    })
}
function dislikeHW (btn) {
    var hwid = $(btn).attr("data-hwid");
    var div = $('#hw_buttons'+hwid);
    $.ajax({
        type: "GET",
        url: "/homework/dislike/",
        dataType: "JSON",
        data: {homework_id: hwid},
        success: function(json) {
            div.find('.Homework_like_count').html(json.likes);
            div.find('.Homework_dislike_count').html(json.dislikes);
            var imgLike = div.find('.like_img');
            var imgDislike = div.find('.dislike_img');
            if (json.disliked) {
                $(imgDislike).attr("src", "../images/dislike_btn_disliked.png");
                if (json.unliked) {
                    $(imgLike).attr("src", "../images/like_btn.png");
                }
            }
            else {
                $(imgDislike).attr("src", "../images/dislike_btn.png");
            }
        }
    })
}