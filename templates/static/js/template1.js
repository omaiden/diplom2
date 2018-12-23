$(function() {
	$(".loginform").hide();
	$(".login").click(function(event) {
		$(".loginform").show();
	});
	$(".close").click(function(event) {
		$(".loginform").hide();
	});
});
