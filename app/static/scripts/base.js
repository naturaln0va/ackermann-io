
var searchField = document.getElementById("search");
searchField.addEventListener('keyup', function(e) {
	if (e.keyCode === 13) {
		window.location.href = '/search/results/' + searchField.value;
	}
}, false);
