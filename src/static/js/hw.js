function likeHW () {
	console.log("Hey");
	var hwid = $(this).attr("data-hwid");
	$.ajax({
		type: "GET",
		url: "{% url like_hw %}",
		dataType: "JSON",
		async: true,
		data: {homework_id: hwid},
		success: function(json) {
			$('#like_count'+hwid).html(json.likes);
		}
	})
}