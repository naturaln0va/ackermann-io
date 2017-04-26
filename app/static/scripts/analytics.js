
var searchField = document.getElementById("search");
searchField.addEventListener('keyup', function(e) {
	if (searchField.value.length == 0) {
		return;
	}
	if (e.keyCode === 13) {
		window.location.href = '/analytics/' + searchField.value;
	}
}, false);