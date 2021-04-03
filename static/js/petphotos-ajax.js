$(document).ready(function() {
	$('#like_btn').click(function() {
		var catepictureIdVar;
		catepictureIdVar = $(this).attr('data-pictureid');
		
		$.get('/rango/like_picture/',
			{'picture_id': catepictureIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
			})
	});
});
