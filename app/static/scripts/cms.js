
function buttonClicked(elem) {
	var result = confirm("Are you sure you want to delete '" + elem.name + "'?");
	if (result == true) {
		window.location.href = '/cms/rm/' + elem.name;
	}
}