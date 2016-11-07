
function buttonClicked(elem) {
	if (elem.value == 'Delete') {
		var result = confirm("Are you sure you want to delete '" + elem.name + "'?");
		if (result == true) {
			window.location.href = '/cms/rm/' + elem.name;
		}
	}
	else if (elem.value == 'Copy') {
		window.prompt("Copy to clipboard: ⌘+C, Return", "/static/assets/" + elem.name);
	}
}